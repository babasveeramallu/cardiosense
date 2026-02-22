# iOS Shortcuts Setup for Apple Watch Integration

## Step 1: Create the Shortcut on iPhone

1. Open **Shortcuts** app on iPhone
2. Tap **+** to create new shortcut
3. Add these actions in order:

### Actions to Add:

**Action 1: Ask for Heart Rate**
- Tap search bar at bottom
- Type "Ask for Input"
- Tap "Ask for Input" action
- Change prompt to: "What is your heart rate?"
- Change Input Type to: "Number"

**Action 2: Set Variable**
- Search "Set Variable"
- Name it: "HR"
- It will use the input from previous step

**Action 3: Ask for SpO2**
- Add "Ask for Input" again
- Prompt: "What is your oxygen saturation?"
- Input Type: "Number"

**Action 4: Set Variable**
- Name it: "SpO2"

**Action 5: Create Dictionary**
- Search "Dictionary"
- Tap "Add new item" to add these keys:
  - Key: `heart_rate` → Value: tap and select variable "HR"
  - Key: `blood_pressure_systolic` → Value: type `120`
  - Key: `blood_pressure_diastolic` → Value: type `80`
  - Key: `oxygen_saturation` → Value: select variable "SpO2"
  - Key: `temperature` → Value: type `37.0`

**Action 6: Get Contents of URL**
- Search "Get Contents of URL"
- Tap "URL" field → type: `http://192.168.12.195:8000/analyze`
- Tap "Show More" button
- Change Method to: **POST**
- Under Headers, tap "Add new field":
  - Key: `Content-Type`
  - Value: `application/json`
- Under Request Body, select: **Dictionary** (from step 5)

**Action 7: Show Notification**
- Search "Show Notification"
- In the text field, tap and select "Contents of URL"

## Step 2: Run the Shortcut

- Tap the shortcut to run manually
- Or use Siri: "Hey Siri, run CardioSense"
- Add to Home Screen widget

## Step 3: Automate (Optional)

1. Go to **Automation** tab in Shortcuts
2. Create **Personal Automation**
3. Trigger: Time of Day (every hour)
4. Action: Run your CardioSense shortcut
5. Disable "Ask Before Running"

## Limitations

- Apple Watch doesn't measure blood pressure (defaults to 120/80)
- Heart rate and SpO2 work on most Apple Watches
- iPhone must be on same WiFi as Pi

## Testing

Make sure iPhone is on WiFi with Pi (192.168.12.195).
Run shortcut - you should see risk analysis notification.
