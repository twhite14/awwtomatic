# awwtomatic
Current Version: 0.4
Automatically obtain pictures of adorable animals from /r/aww.

This script utilizes urllib and some basic knowledge of the reddit source code to obtain links to images of cute animals. urllib is used to then pull down the images from imgur. Once an image is fetched, its ID is added to a list in order to only grab any given image once.
Some aspects of this script are not entirely efficient. A future version will improve on this issue. For example, in order to check if an image is animated, the imgur source code of the appropriate page is obtained and searched.
This script could probably be reused for other subreddits that contain mostly imgur links. A future version will simplify this ability.
The script does not currently gather images from albums. A future version will clear this issue.

## Requirements:
The user must create a directory "downloads" in the same directory as the script. This requirement will be removed in a future version.
Please alter the user-agent (line 11) to reflect your user information.

## Execution:
Execute the script once from the command line to determine whether the script works properly. Once it's confirmed to behave as expected the script can be automated using Windows Task Scheduler. 
For the sake of suppressing the console window, I would recommend altering the file extension to .pyw and executing the script with pythonw.exe. Guides to using Windows Task Scheduler can be easily found online.
This script has been tested on Windows 8.1 on two machines. Performance is not guaranteed on other platforms (but is likely to work on Windows platforms without issue).
