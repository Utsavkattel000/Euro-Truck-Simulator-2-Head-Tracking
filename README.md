# Linux Head Tracking for Euro Truck Simulator 2 (Proton)

This guide explains how to use a custom MediaPipe Python script alongside the Windows version of Opentrack running inside Steam's Proton sandbox to get head tracking working flawlessly in Euro Truck Simulator 2 (ETS2).

## How it Works
1. Your custom Python script tracks your face via webcam and transmits coordinates via UDP.
2. The `opentrack-launcher` script injects and runs the **Windows native version of Opentrack** inside the exact same Proton prefix container as ETS2.
3. Because Opentrack runs inside the Windows simulation layer alongside the game, the game can easily pick up the tracking data using Windows-native tracking protocols (`freetrack 2.0 Enhanced`).

---

## Prerequisites

Before configuring Steam, make sure you have installed your Python dependencies:

    pip install -r requirements.txt

Ensure that the tracking script works and your `face_landmarker.task` file is in the correct directory.

---

## Step-by-Step Setup Guide

### Step 1: Install Opentrack Launcher
`opentrack-launcher` automates downloading the Windows portable version of Opentrack and spinning it up inside your game's active Proton sandbox.

Run the following command to download and place the wrapper script into your local binaries directory:

    mkdir -p ~/.local/bin && wget https://raw.githubusercontent.com/VolatileMark/opentrack-launcher/master/opentrack-launcher -O ~/.local/bin/opentrack-launcher && chmod +x ~/.local/bin/opentrack-launcher

---

### Step 2: Configure Steam Launch Options
We use the launch option to intercept the game's startup, launch Windows Opentrack first, and then run the game in that same environment.

1. Open **Steam** and right-click **Euro Truck Simulator 2** -> **Properties**.
2. Under the **General** tab, scroll down to **Launch Options**.
3. Paste the following exact line:

    ~/.local/bin/opentrack-launcher %command%

---

### Step 3: Configure the Windows Opentrack UI (First Run)
1. Start your game normally from Steam.
2. Because of the launch option, the **Windows version of Opentrack** will open up first inside a Proton window before the game boots.
3. Change the following settings in Opentrack:
   * **Input:** Change this to `UDP over network`.
   * Click the settings (hammer) icon next to Input and make sure the port matches your Python script (`4242`).
   * **Output:** Change this to `freetrack 2.0 Enhanced`.
4. Click **Start** in the Opentrack window to begin listening.

---

### Step 4: Running the Setup Moving Forward

Every time you want to play from now on, follow this simple order:

1. **Fire up the Python Tracker:**
   Start your webcam tracking feed script:
   
       ./track.sh
       
2. **Launch ETS2 from Steam:**
   Opentrack's Windows interface will pop up. Verify the pink octopus moves when you move your head.
3. **Play:**
   Once verified, let the game completely boot up. Your in-game cabin camera will now natively mirror your head movements!
   
   
   Includes pre-trained models provided by Google LLC under the Apache License 2.0.
