# mri_dicom_checker
 a command-line tool that unpacks a ZIP or CAB archive into a temp folder, strips spaces and “#” from all filenames, recursively finds every DICOM (.dcm) file, runs dcmftest to bucket them into valid or corrupt lists, writes those lists to two CSVs, and then cleans up the temp directory.
