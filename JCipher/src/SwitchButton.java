package src;

import java.awt.*;
import javax.swing.*;
import javax.swing.border.Border;

public class SwitchButton extends JButton { // Class extends JButton to retain original functions
	private static final long serialVersionUID = 5690816006327023121L;

	// Borders [Presssed/Not Pressed]
	private final Border defaultBorder = BorderFactory.createLineBorder(Shared.blueGrey, 1);
	private final Border pressBorder = BorderFactory.createLineBorder(Shared.blueGrey, 2);

	private Boolean isPressed = false;
	public void setPressed(Boolean status) { // Change press status based on boolean given
		if (status) { // Change button to pressed color/border
			setBackground(Shared.lightBlue);
			setBorder(pressBorder);

		} else { // Change button to unpressed color/border
			setBackground(Shared.lightGrey);
			setBorder(defaultBorder);
		}

		isPressed = status;
	}

	public Boolean getPressed() {
		return isPressed;
	}
}

// OxygenCobalt