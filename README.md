# nepular
Script for helping Guliang on his work.


this app reads target file list from the specified name-list file, searches them in src dir
then copies hit files into output path, it also lists those were missing.


# How to use
nepular.exe {name_list_file} {dir_you_want_to_search} [output_path]


# Content of name-list file
>    ext .png .jpg .mpeg .txt // the file extens you are interested in, 'ext' is preserved.
>    name0
>    name1
>    name2
>    name3
>    ...


# Output
by default, the ourput dir is ./nepular_result.
