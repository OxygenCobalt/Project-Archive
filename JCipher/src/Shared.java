// Shared
// Equivelent of public.py in my earlier projects, a space for variables used by multiple classes

package src;

// Import Swing elements and Border elements
import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.EtchedBorder;

// Import AWT classes and Clipboard interfaces
import java.awt.*;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;

public class Shared {
	// The key is a raw string split into an array
	// A letter is found on it and then a rotation is added to return a new letter from the array
	public static String[] key = "]!qnk;D\\F}lHhXovx:C*1su>mLG@f$\"E)O'{&,AZYj2+KyV(6[dp7i0JS? `-MNP/|TW3cQI84^=UzaB%btg#<R.e5w~9r_".split("(?!^)");

	// Colors
	// Primarily used to mimick UI elements [Make disabled elements look better, make swap buttons look pressed]
	public static Color lightBlue = new Color(184, 207, 229);
	public static Color lightGrey = new Color(238, 238, 238);
	public static Color blueGrey = new Color(122, 138, 153);

	public static Border normalBorder = BorderFactory.createLineBorder(blueGrey, 1); // Border used in text fields/text areas

	// Fonts
	// HeaderFont is a bold font used for guidance text
	// plainFont is used for everything else
	public static Font headerFont = new Font(Font.SANS_SERIF, Font.BOLD, 15);
	public static Font plainFont = new Font(Font.DIALOG, Font.PLAIN, 12);

	// Primary spin model, starts at 1 and ends at the maximum rotation [Excluding loopover]
	public static SpinnerModel mainSpinModel = new SpinnerNumberModel(
		1,
		1,
		(Shared.key.length - 1),
		1
	);

	public static int findKeyIndex(String toFind) { // Searches the key to find the specific letter, and returns that index
		int i = 0;

		for (String value : key) {
			if (value.equals(toFind)) { // If the element in key exactly equals the lettere
				return i; // Return that index
			}

			i++; // Otherwise check next index
		}

		return -1; // Return -1 if nothing is found to throw an exception
	}

	public static void changeEnabled( // Somewhat ugly function that allows me to disable multiple elements at once
		Boolean enabled,
		JCheckBox checkbox, 
		JSpinner spinner, 
		JTextField textField, 
		JButton... buttons
		) {
		// There can be multiple buttons passed to this at once, so changeEnabled iterates through them
		for (JButton button : buttons) {
			if (button != null) { // Filter array to prevent a NullPointerException
				button.setEnabled(enabled);
			}
		}

		// Change enable status of other items
		// If argument passed to them is null, changeEnabled will change nothing
		if (checkbox != null) {
			checkbox.setEnabled(enabled);
		}

		if (spinner != null) {
			spinner.setEnabled(enabled);
		}

		if (textField != null) {
			textField.setEditable(enabled);
		}
	}

	public static void copy(JTextArea textArea) { // Funciton that copies text from the output box into the clipboard
		String outputText = textArea.getText();
		StringSelection outputSelection = new StringSelection(outputText); // Get the string selection to pass into the clipbaord

		// Find system clipboard and add selection, copying the text
		Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
		clipboard.setContents(outputSelection, null);
	}
}

// OxygenCobalt