## Features

- Easy-to-use custom controls (e.g., DropDown)
- Clean, readable code (Maybe not LOL)
- Designed for extensibility (more controls coming soon)

## Usage

Each control can be imported and used in your Flet app.  
See the code comments and examples in each file for details.

## Controls

- `DropDown.py` — Custom drop-down menu with overlay selection

  **Parameters:**
  - `height` (float): Height of the DropDown (default: 40)
  - `width` (float): Width of the DropDown (default: 70)
  - `menu_text_style` (ft.TextStyle): Style for the displayed text (default: `ft.TextStyle(size=15, color='white,0.8')`)
  - `default_value` (str): Initial displayed value (default: "None")
  - `options` (list[str]): List of selectable options (default: [])
  - `on_select` (callable): Callback function called when an option is selected (default: None)
  - `max_visible` (int): Maximum number of visible options in overlay (default: 3)
  - <img width="264" height="298" alt="image" src="https://github.com/user-attachments/assets/a7842d91-d3b5-4d09-823f-b356ca4f8545" />
