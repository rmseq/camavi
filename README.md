# Camavi

 A *good enough* script to extract [initials](https://en.wikipedia.org/wiki/Initial) from images.
 Some examples can be found [here](./data/).
 
 ## Usage
 
 1) Download the latest release zip file
 2) Extract it somewhere
 3) Execute the file named `Camavi` (`Camavi.exe` in the windows version)
 
By default, all the *.jpg* images in the `data` directory will be processed. The results, an image with the initial cropped and an image with information about what was detected for each image in the directory, will be generated and placed in the same directory. The results will have the naming schemes `<souce name>_res.jpg` and `<source name>_res_debug.jpg`, respectively.

Alternatively, you can...
1) Clone this repository or download it as a zip and extract its contents 
2) (Optional) Create and activate a virtual environment
3) Install the requirements in [requirements.txt`](./requirements.txt)
4) Run [`main.py`](./main.py)

## Configuration

The behavior of the script can be slightly adjusted by changing the values in the `config.ini`. You must follow the scheme already defined and save the file when you are done. By default it uses [this](./config.ini) values.

The `min_area` field is defined as a value that is used to discard small detections. Honestly, it's tricky to select an ideal value and it changes from book to book but very small values will increase the number of false positives and very big values will increase the number of false positives. In general, you must define a  *good enough* value. 

In `input_ext` you can select the extension of the source images. I personally tested *.png* and *.jpeg* images but other extensions used by images (no .pdf support, sorry) may be supported. 

In `show_debug` you can turn off/on the creation of the result with information about what was detected. By default, it is generated because I found it interesting but you may expect better performance if it is set to off. 

Under `[Margins]` you can change the values of the margins applied to the source images, which is important because some books have black bars around the pages from the scan and this can impact the detection of the initials, and the result images (which is obviously desirable). 

Under `[Paths]` you can change from where the script will retrieve the images to be processed and where it will place the results. 

## Disclaimers

The script is programmed to search for one initial per image. If an image has more than one, only one of them will be detected. I may change this in the future. 

Some initials may fail to be detected (false negative) and some images without an initial may return results (false positive). This can be partially mitigated by adjusting the value `min_area` in the `config.ini` file, to learn more about config see section [Configuration](#configuration). 

## Errors, bugs, and contributions 

Feel free to open an issue, request features, or make pull requests in this repository. 
 
