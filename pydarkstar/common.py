import logging
import shutil
import os
import re

def backup(path, copy=False):
    """
    Create backup file name.

    :param path: path of file
    :param copy: perform copy file
    """
    old_path = os.path.abspath(os.path.expanduser(path))

    # nothing to backup
    if not os.path.exists(old_path):
        return ''

    if not os.path.isfile(old_path):
        raise RuntimeError('can only backup files: %s' % old_path)

    # extract file info
    dname, bname = os.path.dirname(old_path), os.path.basename(old_path)
    root, dirs, files = next(os.walk(dname))

    # look for existing backups
    regex = re.compile('^{}(\.(\d+))?$'.format(bname))
    found = []
    for f in files:
        match = regex.match(f)
        if match:
            try:
                found.append(int(match.group(2)))
            except TypeError:
                found.append(0)

    # should of at least found 1 if the file exists
    if not found:
        raise RuntimeError('can not backup file: %s' % old_path)

    # create backup name
    new_path = os.path.join(dname, '{}.{}'.format(bname, max(found) + 1))

    # validate old_path
    if os.path.exists(new_path) or new_path == old_path:
        raise RuntimeError('can not backup file: %s' % old_path)

    # copy the file
    if copy:
        logging.debug('backup (old): %s', old_path)
        logging.debug('backup (new): %s', new_path)
        shutil.copy(old_path, new_path)

    return new_path

def findFiles(top, regex=r'.*', r=False, ignorecase=True, **kwargs):
    """
    Search for files that match pattern.

    :param top: top level directory
    :param regex: pattern to match
    :param r: recursive search
    """
    if ignorecase:
        regex = re.compile(regex, re.IGNORECASE)
    else:
        regex = re.compile(regex)

    if r:
        for root, dirs, files in os.walk(top, **kwargs):
            for f in files:
                match = regex.match(f)
                if match:
                    yield os.path.join(root, f)
    else:
        root, dirs, files = next(os.walk(top, **kwargs))
        for f in files:
            match = regex.match(f)
            if match:
                yield os.path.join(root, f)

if __name__ == '__main__':
    pass