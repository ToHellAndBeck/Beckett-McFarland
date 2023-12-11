import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox
from PyQt5.QtGui import QFont
import csv

class PokemonSelectorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pokémon Selector")
        self.setGeometry(100, 100, 400, 200)

        # Load Pokémon data from CSV
        self.pokemon_data = self.load_pokemon_data()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        scale = 25
        # Create the first dropdown for Pokémon types
        self.type_label = QLabel("Select Type:")
        self.type_label.setFont(QFont("Arial", scale))  # Set font size
        self.type_dropdown = QComboBox(self)
        self.type_dropdown.addItems(self.get_unique_types())
        self.type_dropdown.setFont(QFont("Arial", scale))  # Set font size
        self.type_dropdown.currentIndexChanged.connect(self.update_pokemon_list)

        # Create the second dropdown for Pokémon names
        self.pokemon_label = QLabel("Select Pokémon:")
        self.pokemon_label.setFont(QFont("Arial", scale))  # Set font size
        self.pokemon_dropdown = QComboBox(self)
        self.pokemon_dropdown.setFont(QFont("Arial", scale))  # Set font size

        layout.addWidget(self.type_label)
        layout.addWidget(self.type_dropdown)
        layout.addWidget(self.pokemon_label)
        layout.addWidget(self.pokemon_dropdown)

        self.setLayout(layout)

    def load_pokemon_data(self):
        # Read Pokémon data from the CSV file
        with open('pokelist/pokemon.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    def get_unique_types(self):
        # Get unique Pokémon types from the loaded data
        return list(set(pokemon['Type 1'] for pokemon in self.pokemon_data))

    def update_pokemon_list(self):
        selected_type = self.type_dropdown.currentText()

        # Filter Pokémon based on the selected type
        pokemons_of_type = [
            pokemon['Name'].capitalize()
            for pokemon in self.pokemon_data
            if pokemon['Type 1'].lower() == selected_type.lower()
        ]

        # Update the second dropdown with the Pokémon names
        self.pokemon_dropdown.clear()
        self.pokemon_dropdown.addItems(pokemons_of_type)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PokemonSelectorApp()
    window.show()
    sys.exit(app.exec_())
