<p align="center">
  <img width="240" height="240" src="res/logov2.png">
 </p>
<h3 align="center">A visible, persistent and more forgiving clipboard.</h3>

- greater copy efficiency : The gain in time accumulates with the number of discrete parts. If *t* is the time for switching active windows and *n* is the number of discrete sections of text to be copied, the total time saved is around *(n-1) x t*, which is assuming that the source and destination remain fixed.

- making cohesive notes from multiple documents made easier : copy multiple portions of text independently from multiple documents, without having to change your active window to paste the previously copied text, a faster and hassle-free way to extract what is essential.

- copying code from multiple links : eliminate the frustration of having borrowed a code snippet or workaround from a browser tab, losing it by mis-typing or copying something else, only to realise you've 

- greater fault tolerance for pressing the wrong hotkeys.

- greater visibility : select which of the sections of copied text you want to paste on-the-fly and never get it wrong.

- persistent history : make your clipboard history persistent across sessions and shutdowns for easier recovery.

- cross-platform : support for efficient text manipulation on Windows as well as Linux systems.

- fully-functional on all popular text-crunching tools: Office, LibreOffice, Sublime Text and more.

## Dependencies

For executing the desktop app, the following packages must be installed:
* tkinter
* pynput
* clipboard

Use pip3 to install the requirements:

```sh
$ pip3 install -r requirements.txt
```

After installing run the following command in the desktop directory: 
The latest version is in : withui/octopaste.py

```sh
$ python3 octopaste.py
```


## Usage
Execute:

```python octopaste.py```

- To copy from any documents, pdf, browser etc use:```Ctrl + C```

- To copy from Terminal use:```Ctrl + Shift + C```


- To paste in any documents, pdf, browser etc use:```Ctrl + Alt + B```

- To paste in the Terminal:```Ctrl + Alt + Shift + B```

A pop up will be generated. Now select the text you want to paste and press Enter to paste the text.

The default maximum number of clipboard text segments in the OP pop-up have been set to 10. This can be changed with ease by modifying the following in octopaste.py:

```self.MAX_ENTRIES = <number of entries as an integer value>```

## Demonstration

Click the below video to view an example of the usage:

<p align="center">
    <a href = "https://drive.google.com/file/d/1M0Zruh_Q50UU5jgDcfJDrXDtrY9mrbar/view?usp=sharing">
      <img width="150" height="150" src="res/playbutton.png" alt = "link to video">
    </a>
 </p>
 
## Coming Soon:

File System manipulation made easier with a similar approach.

## Contributors
* Chirag Trasikar - [chirag16](https://github.com/chirag16)
* Ankit Shah - [ankitcshah14](https://github.com/ankitcshah14)
* Arpita Hegde - [arpitahegde414](https://github.com/arpitahegde414)
* Apoorva Gokhale - [apoorva-21](https://github.com/apoorva-21)
