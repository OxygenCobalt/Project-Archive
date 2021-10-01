// EncodePanel
// Panel for encoding messages, split off from the main function

package src;

// Swing/AWT elements
import javax.swing.*;

import java.awt.*;
import java.awt.event.*;

import java.util.Random; // Random rotations for encoding

// Assigning checkbox icons
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;

public class EncodePanel extends JPanel implements ActionListener { // Class extends JPanel, JFrames cant be nested within eachother as they are windows
	private static final long serialVersionUID = 5690816006327023121L; // Because I'm extending JPanel, I need to add a serial to prevent a warning

	// Checkbox icons, I cant directly define them as they need a try/catch to be added
	private ImageIcon unselected;
	private ImageIcon selected;

	// Encode UI elements
	private JLabel encodeText = new JLabel();
	private JTextField encodeEntry = new JTextField();
	private JButton encodeButton = new JButton();
	private JCheckBox randomToggle = new JCheckBox();
	private JSpinner encodeSpinner = new JSpinner(Shared.mainSpinModel);
	private JTextArea encodeOutput = new JTextArea();
	private JButton encodeCopy = new JButton();
	private JButton encodeClear = new JButton();

	public void config() {
		// Load checkbox icons in
		// Checkboxes take the images as an ImageIcon class, requiring a conversion
		try {
			unselected = new ImageIcon(ImageIO.read(new File("./res/unchecked.png")));
			selected = new ImageIcon(ImageIO.read(new File("./res/checked.png")));
		} catch (IOException e) {
			System.out.println("Cant find icons");
		}

		setBounds(0, 0, 400, 400);
		setLayout(null);

		// Configuration [Placement, text, colors, fonts]
		encodeText.setText("Place text to encode here");
		encodeText.setBounds(92, 10, 212, 30);
		encodeText.setFont(Shared.headerFont);
		encodeText.setForeground(Color.BLACK);

		encodeEntry.setBounds(97, 40, 202, 20);
		encodeEntry.setBorder(Shared.normalBorder);

		encodeButton.setText("Encode!");
		encodeButton.setBounds(97, 81, 100, 27);
		encodeButton.setFont(Shared.plainFont);
		encodeButton.setFocusPainted(false);
		encodeButton.setBackground(Shared.lightGrey);
		encodeButton.addActionListener(this); // Add button actions

		randomToggle.setText("Random");
		randomToggle.setBounds(215, 71, 100, 20);
		randomToggle.setFont(Shared.plainFont);
		randomToggle.setFocusPainted(false); // Remove strange borders from button text
		randomToggle.addActionListener(this);

		// Set checkbox icons
		randomToggle.setIcon(unselected);
		randomToggle.setSelectedIcon(selected);

		encodeSpinner.setBounds(226, 96, 53, 18);
		encodeSpinner.setBackground(Shared.lightGrey);
		encodeSpinner.setBorder(Shared.normalBorder);
		encodeSpinner.setEditor(new JSpinner.DefaultEditor(encodeSpinner)); // Disable spinbox editing to prevent changing the number to something invalid.

		encodeOutput.setBounds(48, 129, 300, 200);
		encodeOutput.setFont(Shared.plainFont);
		encodeOutput.setBackground(Color.WHITE);
		encodeOutput.setBorder(Shared.normalBorder);

		// Textbox Configuration
		encodeOutput.setEditable(false);
        encodeOutput.setLineWrap(true); // Long messages will not go past the bounds of the box

		encodeCopy.setText("Copy");
		encodeCopy.setBounds(100, 339, 100, 30);
		encodeCopy.setFont(Shared.plainFont);
		encodeCopy.setFocusPainted(false);
		encodeCopy.setBackground(Shared.lightGrey);
		encodeCopy.addActionListener(this);

		encodeClear.setText("Clear");
		encodeClear.setBounds(200, 339, 100, 30);
		encodeClear.setFont(Shared.plainFont);
		encodeClear.setFocusPainted(false);
		encodeClear.setBackground(Shared.lightGrey);
		encodeClear.addActionListener(this);

		// Disable encodeCopy/encodeClear, as they are only enabled when a message is encoded
		Shared.changeEnabled(false, null, null, null, encodeCopy, encodeClear);
    }

	public void build() {
		// Add all items to panel
		add(encodeText);
		add(encodeEntry);
		add(encodeButton);
		add(randomToggle);
		add(encodeSpinner);
		add(encodeOutput);
		add(encodeCopy);
		add(encodeClear);
	}

	private String encode() { // Encodes messages based on the "Cipher"
		Random rand = new Random();

		// Split inputted message into an array, and create 
		// an output array the same length that the new letters will go into
		String[] toEncode = encodeEntry.getText().split("(?!^)");
		String[] encoded = new String[toEncode.length];

		int rotation;
		int index;
		int i = 0; // Output index

		// Determine if random is on/off
		if (randomToggle.isSelected()) {
			do {
				rotation = rand.nextInt(Shared.key.length); // If so, generate a new integer in bounds of the key length
			} while (rotation == 0);
		} else {
			rotation = (Integer) encodeSpinner.getValue(); // Otherwise, get the value from the spinner
		}

		// Main encoding iteration
		for (String character : toEncode) {
			index = Shared.findKeyIndex(character);

			if (index < 0) { // If character finding failed [Returns -1, result of an illegal character]
				throw new java.lang.RuntimeException(
					"Character in string was not found in key." // Throw basic exception and call off encoding
				);
			}

			index = (index + rotation) % Shared.key.length; // Rotate letters [With rollover]

			encoded[i] = Shared.key[index]; // Add letter to output string

			i++; // Update output index
		}

		String toReturn = String.join("", encoded); // Join output string together to return

		if (!toReturn.equals("null")) {
			// Disable encode input options [Really just a design choice]
			// Enable copy/clear functions, now that theres an output
			Shared.changeEnabled(false, randomToggle, encodeSpinner, encodeEntry, encodeButton);
			Shared.changeEnabled(true, null, null, null, encodeCopy, encodeClear);

			return toReturn;
		}

		return ""; // If toReturn is empty [null], then just return a blank string
	}

	// Wipe all values and enabled statuses from panel
	// Occurs when Clear is pressed or panel is swapped
	public void reset() {
		randomToggle.setSelected(false);
		encodeSpinner.setValue(1);
		encodeEntry.setText("");
		encodeOutput.setText("");

		// Reenable decode input, disable copy/clear now that output is gone
		Shared.changeEnabled(true, randomToggle, encodeSpinner, encodeEntry, encodeButton);
		Shared.changeEnabled(false, null, null, null, encodeCopy, encodeClear);
	}

	public void actionPerformed(ActionEvent event) {
		String type = event.getActionCommand(); // Get text of button to determine action

		// Input is checked to see if it actually has text in it
		if (type.equals("Encode!") && !encodeEntry.getText().equals("")) {
			encodeOutput.setText(encode());
		}

		else if (type.equals("Random")) {
			// Disable/Enable spinner based on its previous state
			// Creates the effect of the checkbox disabling the spinner
			if (!encodeSpinner.isEnabled()) {
				Shared.changeEnabled(true, null, encodeSpinner, null);
			} else {
				Shared.changeEnabled(false, null, encodeSpinner, null);
			}
		}

		else if (type.equals("Copy")) {
			Shared.copy(encodeOutput);
		}

		else if (type.equals("Clear")) {
			reset();
		}
	}
}

// OxygenCobalt