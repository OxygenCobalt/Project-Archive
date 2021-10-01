// JCipher
// Clone of my old PyCipher program, now in Java + Swing

// Import UI Libraries
import javax.swing.*;

import java.awt.*;
import java.awt.event.*;

import src.*; // Import auxillary library

@SuppressWarnings("deprecation") // I'm forced to use "new Integer()" do swap layers, hence the suppression
public class JCipher extends JFrame implements ActionListener { // Class implements ActionListener to allow a centralized actionPerformed function [Looks nicer]
	private static final long serialVersionUID = 5690816006327023121L; 	// Serial ID [For Semantics]

	private final Image icon = Toolkit.getDefaultToolkit().getImage("./res/icon.png"); // Load window icon

	// Define swap buttons
	// These change the frame from Encode/Decode depending on which one is clicked
	private SwitchButton encodeActivateButton = new SwitchButton();
	private SwitchButton decodeActivateButton = new SwitchButton();

	// Define main panels, which are their own classes
	private JLayeredPane main = new JLayeredPane();
	private EncodePanel encodePanel = new EncodePanel();
	private DecodePanel decodePanel = new DecodePanel();

	public JCipher() {
		// Configurate all UI elements
	    encodePanel.config();
	    decodePanel.config();
	    config();

	    // Add all UI elements to window
	    encodePanel.build();
	    decodePanel.build();
		build();
	}

	public static void main(String cmdArgs[]) {
		new JCipher();
	}
	
	private void config() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // Prevent java process from running after window close
		setLocationRelativeTo(null); // Make window appear at the center of the screen
		setResizable(false); // Window isnt recisable since I like using Pixel Placement
		setTitle("JCipher");
		setIconImage(icon);
		setSize(400, 420);
		setLayout(null); // I like using pixel placement instead of layouts

		// Configure layered parent frame
		main.setBounds(0, 20, 400, 400);
		main.setLayout(null);

		// Configure swap buttons
		// Their configurations near-identical, but I cant do them both at the same time.
		encodeActivateButton.setText("Encode");
		encodeActivateButton.setBounds(0, 0, 200, 30);
		encodeActivateButton.setFont(Shared.plainFont);
		encodeActivateButton.setFocusPainted(false); // Prevent a strange border from appearing around the button text
		encodeActivateButton.addActionListener(this); // Add button action [this is used because of the implemented class]
		encodeActivateButton.setPressed(true); // Call custom pressed function, as swing doesn't support this conventionally

		decodeActivateButton.setText("Decode");
		decodeActivateButton.setBounds(200, 0, 196, 30);
		decodeActivateButton.setFont(Shared.plainFont);
		decodeActivateButton.setFocusPainted(false);
		decodeActivateButton.addActionListener(this);
		decodeActivateButton.setPressed(false);
	}

	private void build() {
		// Add encode/decode panels [Encode is always default]
		main.add(encodePanel, new Integer(1));
		main.add(decodePanel, new Integer(0));

		// Add frame buttons/layer frame
		add(encodeActivateButton);
		add(decodeActivateButton);
		add(main);

		setVisible(true); // Start window
	}

	private void switchPanels(String buttonType) { // Switch panels based on which swap button was pressed
		if (buttonType.equals("Encode")) {
			if (!encodeActivateButton.getPressed()) { // Check if button is already "Pressed" to prevent redundant presses

				// Swap button press states
				encodeActivateButton.setPressed(true);
				decodeActivateButton.setPressed(false);

				encodePanel.reset(); // Clear panel [To prevent conflicts between the shared spinbox values]

				// Swap encode/decode layers
				main.setLayer(encodePanel, new Integer(1));
				main.setLayer(decodePanel, new Integer(0));
			}
		} else if (buttonType.equals("Decode")) {
			if (!decodeActivateButton.getPressed()) {
				decodeActivateButton.setPressed(true);
				encodeActivateButton.setPressed(false);

				decodePanel.reset();

				main.setLayer(encodePanel, new Integer(0));
				main.setLayer(decodePanel, new Integer(1));
			}
		}
	}

	public void actionPerformed(ActionEvent event) {
		switchPanels(event.getActionCommand()); // Pass button text ["Encode" or "Decode"] instead of an if/else
	}
}

// OxygenCobalt