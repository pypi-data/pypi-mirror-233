# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from perian.paths.selection_get_flavors import Api

from perian.paths import PathValues

path = PathValues.SELECTION_GETFLAVORS