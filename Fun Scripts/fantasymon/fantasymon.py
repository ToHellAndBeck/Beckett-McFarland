import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox
from PyQt5.QtGui import QFont, QPixmap
import csv
import os

class PokemonSelectorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pokémon Selector")
        self.setGeometry(100, 100, 400, 400)

        # Load Pokémon data from CSV
        self.pokemon_data = self.load_pokemon_data()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create the first dropdown for Pokémon types
        self.type_label = QLabel("Select Type:")
        self.type_label.setFont(QFont("Arial", 12))  # Set font size
        self.type_dropdown = QComboBox(self)
        self.type_dropdown.addItems(self.get_unique_types())
        self.type_dropdown.setFont(QFont("Arial", 12))  # Set font size
        self.type_dropdown.currentIndexChanged.connect(self.update_pokemon_list)

        # Create the second dropdown for Pokémon names
        self.pokemon_label = QLabel("Select Pokémon:")
        self.pokemon_label.setFont(QFont("Arial", 12))  # Set font size
        self.pokemon_dropdown = QComboBox(self)
        self.pokemon_dropdown.setFont(QFont("Arial", 12))  # Set font size
        self.pokemon_dropdown.currentIndexChanged.connect(self.display_pokemon_info)

        # Labels for displaying Pokémon information and sprite
        self.info_labels = [QLabel("", self) for _ in range(7)]
        self.sprite_label = QLabel(self)

        layout.addWidget(self.type_label)
        layout.addWidget(self.type_dropdown)
        layout.addWidget(self.pokemon_label)
        layout.addWidget(self.pokemon_dropdown)

        # Add labels for displaying Pokémon information
        for label in self.info_labels:
            layout.addWidget(label)

        # Add label for displaying Pokémon sprite
        layout.addWidget(self.sprite_label)

        self.setLayout(layout)

    def load_pokemon_data(self):
        # Read Pokémon data from the CSV file
        with open('pokemon.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    def get_unique_types(self):
        # Get unique Pokémon types from the loaded data
        return list(set(pokemon['Type 1'] for pokemon in self.pokemon_data))

    def update_pokemon_list(self):
        selected_type = self.type_dropdown.currentText()

        # Filter Pokémon based on the selected type
        pokemons_of_type = [
            (pokemon['Name'].capitalize(), pokemon['#'])
            for pokemon in self.pokemon_data
            if pokemon['Type 1'].lower() == selected_type.lower()
        ]

        # Update the second dropdown with the Pokémon names and numbers
        self.pokemon_dropdown.clear()
        self.pokemon_dropdown.addItems([f"{pokemon[0]} ({pokemon[1]})" for pokemon in pokemons_of_type])

    def display_pokemon_info(self):
        selected_pokemon_name_and_number = self.pokemon_dropdown.currentText()

        # Extract Pokémon name and number from the selected text
        selected_pokemon_name, selected_pokemon_number = selected_pokemon_name_and_number.split(' (')
        selected_pokemon_number = selected_pokemon_number[:-1]  # Remove the trailing ')'

        # Find the selected Pokémon in the data
        selected_pokemon = next(
            (pokemon for pokemon in self.pokemon_data if pokemon['#'] == selected_pokemon_number),
            None
        )

        if selected_pokemon:
            # Display Pokémon information
            self.info_labels[0].setText(f"Type 1: {selected_pokemon['Type 1']}")
            self.info_labels[1].setText(f"Type 2: {selected_pokemon['Type 2']}")
            self.info_labels[2].setText(f"Total: {selected_pokemon['Total']}")
            self.info_labels[3].setText(f"HP: {selected_pokemon['HP']}")
            self.info_labels[4].setText(f"Attack: {selected_pokemon['Attack']}")
            self.info_labels[5].setText(f"Defense: {selected_pokemon['Defense']}")
            self.info_labels[6].setText(f"Speed: {selected_pokemon['Speed']}")

            # Display Pokémon sprite based on the Pokémon's number
            sprite_path = os.path.join('sprites', f"{selected_pokemon_number}.png")
            if os.path.exists(sprite_path):
                pixmap = QPixmap(sprite_path)
                self.sprite_label.setPixmap(pixmap)
            else:
                self.sprite_label.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PokemonSelectorApp()
    window.show()
    sys.exit(app.exec_())
