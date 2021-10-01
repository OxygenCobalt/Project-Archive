// DecodePanel
// Panel for decoding messages, split off from the main function

package src;

// Import swing/awt elements
import javax.swing.*;
import javax.swing.event.*;

import java.awt.*;
import java.awt.event.*;

// Import IO items for checkbox icons
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;

public class DecodePanel extends JPanel implements ActionListener { // Class extends JPanel, JFrames cant be nested within eachother as they are windows
	private static final long serialVersionUID = 5690816006327023121L; // Because I'm extending JPanel, I need to add a serial to prevent a warning

	// Checkbox icons, I cant directly define them as they need a try/catch to be added
	private ImageIcon unselected;
	private ImageIcon selected;

	// Main list of decoded strings used by output box
	// Used by both brute force and normal rotation
	private String[] decodeList = new String[Shared.key.length - 1];

	// Decode UI Elements
	private JLabel decodeText = new JLabel();
	private JTextField decodeEntry = new JTextField();
	private JButton decodeButton = new JButton();
	private JCheckBox bruteToggle = new JCheckBox();
	private JSpinner decodeSpinner = new JSpinner(Shared.mainSpinModel);
	private JLabel decodeOutputText = new JLabel();
	private JSpinner decodeOutputSpinner = new JSpinner(Shared.mainSpinModel);
	private JTextArea decodeOutput = new JTextArea();
	private JButton decodeCopy = new JButton();
	private JButton decodeClear = new JButton();

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
		decodeText.setText("Place text to decode here");
		decodeText.setBounds(92, 10, 212, 30);
		decodeText.setFont(Shared.headerFont);
		decodeText.setForeground(Color.BLACK);

		decodeEntry.setBounds(97, 40, 202, 20);
		decodeEntry.setBorder(Shared.normalBorder);

		decodeButton.setText("Decode!");
		decodeButton.setBounds(97, 81, 100, 27);
		decodeButton.setFont(Shared.plainFont);
		decodeButton.setFocusPainted(false);
		decodeButton.setBackground(Shared.lightGrey);
		decodeButton.addActionListener(this); // Add button actions

		bruteToggle.setText("Brute Force");
		bruteToggle.setBounds(204, 71, 100, 20);
		bruteToggle.setFont(Shared.plainFont);
		bruteToggle.setFocusPainted(false); // Remove strange borders from button text
		bruteToggle.addActionListener(this);

		// Set checkbox icons
		bruteToggle.setIcon(unselected);
		bruteToggle.setSelectedIcon(selected);

		decodeSpinner.setBounds(226, 96, 53, 18);
		decodeSpinner.setBorder(Shared.normalBorder);
		decodeSpinner.setBackground(Shared.lightGrey);

		// Disable spinbox editing to prevent changing the number to something invalid.
		decodeSpinner.setEditor(new JSpinner.DefaultEditor(decodeSpinner));

		decodeOutputText.setText("Output at rotation");
		decodeOutputText.setBounds(92, 145, 149, 30);
		decodeOutputText.setFont(Shared.headerFont);
		decodeOutputText.setForeground(Shared.lightBlue);

		decodeOutputSpinner.setBounds(252, 152, 52, 18);
		decodeOutputSpinner.setBorder(Shared.normalBorder);
		decodeOutputSpinner.setBackground(Shared.lightGrey);
		decodeOutputSpinner.setEditor(new JSpinner.DefaultEditor(decodeSpinner));

		decodeOutput.setBounds(48, 179, 300, 150);
		decodeOutput.setFont(Shared.plainFont);
		decodeOutput.setBorder(Shared.normalBorder);
		decodeOutput.setBackground(Color.WHITE);

		// Textbox Configuration
		decodeOutput.setEditable(false);
        decodeOutput.setLineWrap(true); // Long messages will not go past the bounds of the box

		decodeCopy.setText("Copy");
		decodeCopy.setBounds(100, 339, 100, 30);
		decodeCopy.setFont(Shared.plainFont);
		decodeCopy.setFocusPainted(false);
		decodeCopy.setBackground(Shared.lightGrey);
		decodeCopy.addActionListener(this);

		decodeClear.setText("Clear");
		decodeClear.setBounds(200, 339, 100, 30);
		decodeClear.setFont(Shared.plainFont);
		decodeClear.setFocusPainted(false);
		decodeClear.setBackground(Shared.lightGrey);
		decodeClear.addActionListener(this);

		// Disable encodeCopy/encodeClear, as they are only enabled when a message is encoded
		// Also disable the output spinner, as it should be enabled only in brute force mode
		Shared.changeEnabled(false, null, decodeOutputSpinner, null, decodeCopy, decodeClear);
	}

	public void build() {
		// Add all items to panel
		add(decodeText);
		add(decodeEntry);
		add(decodeButton);
		add(bruteToggle);
		add(decodeSpinner);
		add(decodeOutputText);
		add(decodeOutputSpinner);
		add(decodeOutput);
		add(decodeCopy);
		add(decodeClear);
	}

	private void decode() { // Decodes messages based on the "Cipher"
		// Split inputted message into an array, and create 
		// an output array the same length that the new letters will go into
		String[] toDecode = decodeEntry.getText().split("(?!^)");
		String[] decoded = new String[toDecode.length];

		int rotation = 1;
		int index;
		int i = 0; // Output index

		// Cap used to swap between the two decode modes
		// If the cap is 1, then it will iterate once [Normal Rotation]
		// If the cap is the full key length, then it will iterate through all values [Brute Force Mode]
		int cap = (Shared.key.length - 1);

		if (!bruteToggle.isSelected()) {
			cap = 1;
			rotation = (Integer) decodeSpinner.getValue(); // Set rotation to spinner value if not in brute force mode
		} else {
			// If brute force is on, enable the text and the spinner
			// This is usually done at the end, but due to the nature of this its here instead.
			decodeOutputText.setForeground(Color.BLACK);
			Shared.changeEnabled(true, null, decodeOutputSpinner, null);
		}

		// Primary decode loop
		for (int j = 0; j<cap; j++) {
			i = 0;

			for (String character : toDecode) {
				index = Shared.findKeyIndex(character);

				if (index < 0) { // If character finding failed [Returns -1, result of an illegal character]
					throw new java.lang.RuntimeException(
						"Character in string was not found in key." // Throw basic exception to call off
					);
				}

				index = (index - rotation); // Change rotation, but in reverse this time.

				// You cant do rollover in reverse with %, so this function is here to do it instead
				if (index < 0) {
					index = Shared.key.length + index;
				}

				decoded[i] = Shared.key[index]; // Add letter to decoded string

				i++;
			}

			decodeList[j] = String.join("", decoded); // Add joined string to decodeList[]
			rotation++; // Add rotation [Wont be used outside of brute force mode]
		}


		decodeOutput.setText(decodeList[0]); // By adding the plain rotation to the array anyway, it will still be displayed

		// Disable decode input options [Really just a design choice]
		// Enable copy/clear functions, now that theres an output
		Shared.changeEnabled(false, bruteToggle, decodeSpinner, decodeEntry, decodeButton);
		Shared.changeEnabled(true, null, null, null, decodeCopy, decodeClear);
	}

	// Wipe all values and enabled statuses from panel
	// Occurs when Clear is pressed or panel is swapped
	public void reset() {
		decodeList = new String[Shared.key.length - 1]; // Reset decodeList to prevent conflicts

		bruteToggle.setSelected(false);
		decodeSpinner.setValue(1);
		decodeEntry.setText("");
		decodeOutput.setText("");
		decodeOutputText.setForeground(Shared.lightBlue); // "Disable" label text by setting it to the same color

		// Reenable decode input, disable copy/clear now that output is gone
		Shared.changeEnabled(true, bruteToggle, decodeSpinner, decodeEntry, decodeButton);
		Shared.changeEnabled(false, null, decodeOutputSpinner, null, decodeCopy, decodeClear);
	}

	public void actionPerformed(ActionEvent event) {
		String type = event.getActionCommand();

		if (type.equals("Decode!")) {
			decode();
		}

		else if (type.contains("Brute")) {
			// Disable/Enable spinner based on its previous state
			// Creates the effect of the checkbox disabling the spinner
			if (!decodeSpinner.isEnabled()) {
				Shared.changeEnabled(true, null, decodeSpinner, null);
			} else {
				decodeSpinner.setValue(1);
				Shared.changeEnabled(false, null, decodeSpinner, null);
			}
		}

		else if (type.equals("Copy")) {
			Shared.copy(decodeOutput);
		}

		else if (type.equals("Clear")) {
			reset();
		}
	}
}

// OxygenCobalt