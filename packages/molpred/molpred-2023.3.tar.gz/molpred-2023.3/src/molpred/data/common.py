#!/usr/bin/env python3
'''
Common elements.
'''

import pathlib


def missing_or_older(targets, references):
    '''
    Return True if any of the target paths are missing or older than the
    reference paths.  This is used to conditionally update files only when
    necessary.

    Args:
        targets:
            An iterable of target paths.

        references:
            An iterable of reference paths. They must exist.

    Returns:
        True if the target file is missing or older, False otherwise.
    '''
    targets = [pathlib.Path(target) for target in targets]
    if not all(target.exists() for target in targets):
        return True
    target_mtime = min(target.stat().st_mtime for target in targets)
    ref_mtime = max(pathlib.Path(path).stat().st_mtime for path in references)
    return target_mtime <= ref_mtime


def tag_path(path, tag, suffix=None):
    '''
    Add a tag to the filename of a path. The tag is inserted just before the
    suffix.

    Args:
        path:
            The path to tag.

        tag:
            The tag to insert.

        suffix:
            If not None then it will replace the suffix of the input path. It
            should contain a period, e.g. ".csv".

    Returns:
        The resulting path as a pathlib.Path object.
    '''
    path = pathlib.Path(path)
    if suffix is None:
        suffix = path.suffix
    return path.parent / f'{path.stem}{tag}{suffix}'
