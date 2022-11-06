<p align="center">
    <img width=100% src="cover.png">
  </a>
</p>
<p align="center"> 🤖 Create vulnerable Android apps for testing & training in seconds. 📱 </p>

<br>

BDF is a Python tool designed to spin-up pseudo random vulnerable Android applications for vulnerability research, ethical hacking, and pen testing Android app practice. 
- To get started, download the dependancies and run ```BrokenDroidFactory.py```, it's as simple as that! ✔️
- Create a pseudo random Android APK that contains an assortment of vulnerable and issue prone code. 💀
- After run, a ```README.md``` file is created detailing the app's issues and vulnerabilities. 📝 

# ➡️ Getting Started 
## Installation 
After cloning the repository all BDF dependencies can be installed manually or via the requirements file, with:

``` bash
pip install -r REQUIREMENTS.txt
```

In addition to the above, you will also need a copy of the Android SDK. If you do not have this already [it can be downloaded here](https://developer.android.com/studio) by either downloading it via Android Studio or downloading it via the command line tools. To ensure that BDF picks up your SDK path perform **one of the following**:
- Save your SDK path to ```C:\Users\<username>\AppData\Local\Android\Sdk``` on Windows.
- Provide the path to your SDK to BDF with the ```-s``` paramiter. 
- Provide the path to your SDK when prompted by the command line.
- Create a file at ```Broken-Droid-Factory/demoapp/local.properties``` with the contents ```sdk.dir=<path to your SDK>```
- Open the Android project ```demoapp``` in AndroidStudio, it will then create a local file called ```local.properties``` detailing your SDK path. 

BDF has only been tested on **Windows 10**.

## Usage
Run BDF with Python:
```bash
python BrokenDroidFactory.py
```

Several optional pramiters can be provided to BDF, use ```-h``` to see a full list:

```
optional arguments:
  -h, --help            Show this help message and exit.
  -o OUTPUT, --output OUTPUT
                        The output directory for the compiled APK to be saved
                        to.
  -t TEMPLATE, --template TEMPLATE
                        The path to the template app. Do not alter unless you
                        know what you're doing.
  -s SDK, --sdk SDK     The path to your local Android SDK.
  -c CHALLENGE, --challenge CHALLENGE
                        The desired challenge level for the created APK.
  -v, --verbose         Increase output verbosity.
```

After running BDF to completion you will be left with 2 files in the output directory (```out``` if not provided). A ```README.md``` file detailing the workings and the types of challenges in the app, and an ```.apk``` file.

# 🏅 Types Of Challenges
Use BDF to create vulnerable and issue prone Android applications in the below categories:
- Broken Crypto: Insecure Algorithm Usage ✅
- Broken Crypto: Predictable Key Material ✅
- Exploitable Exported Activities ✅
- Insecure Data Storage ❌
- Sensitive Data In Memory ✅
- Tapjacking ❌
- Task hijacking ❌

# ⚗️ Creating Your Own Patchers
Patchers are used by BDF to modify a template application source and add vulnerable and issue prone code to it. A patcher must have several key aspects and have this purpose in mind. However, outside of this how patchers are implemented is quite flexible and modular.
- A patcher should be saved to the ```patchers``` directory.
- A patcher should inherit ```patcher_interface.patcher```
- A patcher should have a member variable of ```difficulty``` set to an int value between 0 and 10 - where 0 means it provides no challenge and is used to add variability to the app, and a number higher than 0 denotes it's difficulty score to complete (with the higher the score the more difficult it is).
- A patcher should have a ```patch``` function (of which is automatically run when the patcher is called by BDF) and should return a string based on what the patcher has done.
- A reference to your created patcher class should be added to the ```patcher_list``` list variable in ```BrokenDroidFactory.py```
