import arcade
from random import randrange
class Game:

    def __init__(self):
        print("Game is initialized")

    username = None
    player_dict = dict()
    send_flag = False

    # Card sizing constants
    CARD_SCALE = 0.1
    CARD_WIDTH = 140 * CARD_SCALE
    CARD_HEIGHT = 190 * CARD_SCALE

    # Mat sizing constants
    MAT_PERCENT_OVERSIZE = 6
    MAT_HEIGHT = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)
    MAT_WIDTH = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
    # Mat gap sizes
    VERTICAL_MARGIN_PERCENT = 0.5
    HORIZONTAL_MARGIN_PERCENT = 0.4


    # Screen size
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    # Screen name
    SCREEN_TITLE = "Set card game"


    # The Y value to start placing the deck and found sets mats
    BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

    # The X value to start placing the deck and found sets mats
    START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT
    # The X value to start placing the main mats
    MAIN_START_X = MAT_WIDTH * 2.3
    # The X value to start placing the comparison mats
    SECONDARY_START_X = MAT_WIDTH * 2.8

    # The X value to start placing other players' set piles or set count
    OTHER_PLAYER_START_X = SCREEN_WIDTH - MAT_WIDTH / 2 - MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT 

    # Card constants
    CARD_COLOR = ["Red", "Green", "Purple"]
    CARD_SHAPE = ["Oval", "Squiggle", "Diamond"]
    CARD_FILLING = ["Full", "Shaded", "Empty"]
    CARD_NUMBER = ["One", "Two", "Three"]
    # Face down image
    FACE_DOWN_IMAGE = "images/Face down card.png"



    # The Y value to place main cards
    TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

    MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

    LOW_Y = MIDDLE_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
    # The Y value to place comparison cards
    COMPARISON_Y = LOW_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

    # How far apart each pile goes
    X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT


    class Display(arcade.Window):
        def __init__(self, reset=True):
            if reset == True:
                super().__init__(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT, Game.SCREEN_TITLE)
                # SpriteList with all cards no matter their position
                self.card_list = None
                # Selected card list
                self.selected_cards = None
                # SpriteList with all the mats the cards lay on
                self.pile_mat_list = None
                # Create a list to hold piles
                self.piles = None


                # Username for this player
                self.username = Game.username
                # Set count
                self.set_count = 0

                arcade.set_background_color(arcade.color.DARK_GREEN)


        def setup(self, reset=True):
            """Set up the game. Can be called to reset the game."""
            if reset == True:
                # This while loop prevents you from having to enter your username everytime you press "R" to reset the game.
                # Create username from input. You only enter your username.
                while self.username not in Game.player_dict:
                    # self.username = input("Enter your username (around 10 characters is ideal): ")
                    # The if statement stops you from overwriting someone elses username
                    if self.username not in Game.player_dict:
                        Game.player_dict[self.username] = 0
                    else:
                        print(f"{self.username} is already in the player dictionary.")
                # If this is not the first time playing the game, erase current scores
                for player in Game.player_dict:
                    Game.player_dict[player] = 0


                
                # List of cards selected by mouse
                self.selected_cards = []
                # Original position of cards selected by mouse in case they need to go back
                self.held_cards_original_position = []
                # list of piles to hold cards
                self.piles = [[] for _ in range(18)]

                # Reset set count
                self.set_count = 0

                # Create the mats the cards go on

                # Spritelist with all the mats the cards go on
                self.pile_mat_list = arcade.SpriteList()

                # Create the mats for the bottom face down and face up piles, the deck, and the found sets
                # index 0
                pile = arcade.SpriteSolidColor(Game.MAT_WIDTH, Game.MAT_HEIGHT, arcade.color.GREEN_YELLOW)
                pile.position = Game.START_X, Game.BOTTOM_Y
                self.pile_mat_list.append(pile)

                # index 1
                pile = arcade.SpriteSolidColor(Game.MAT_WIDTH, Game.MAT_HEIGHT, arcade.color.GREEN_YELLOW)
                pile.position = Game.START_X + Game.X_SPACING, Game.BOTTOM_Y
                self.pile_mat_list.append(pile)

                # Create the four top piles
                # indexes 2-5
                for i in range(4):
                    pile = arcade.SpriteSolidColor(Game.MAT_WIDTH, Game.MAT_HEIGHT, arcade.color.GREEN_YELLOW)
                    pile.position = Game.MAIN_START_X + i * Game.X_SPACING, Game.TOP_Y
                    self.pile_mat_list.append(pile)


                # Create the four middle piles
                # indexes 6-9
                for i in range(4):
                    pile = arcade.SpriteSolidColor(Game.MAT_WIDTH, Game.MAT_HEIGHT, arcade.color.GREEN_YELLOW)
                    pile.position = Game.MAIN_START_X + i * Game.X_SPACING, Game.MIDDLE_Y
                    self.pile_mat_list.append(pile)
                
                # Create the four bottom piles
                # indexes 10-13
                for i in range(4):
                    pile = arcade.SpriteSolidColor(Game.MAT_WIDTH, Game.MAT_HEIGHT, arcade.color.GREEN_YELLOW)
                    pile.position = Game.MAIN_START_X + i * Game.X_SPACING, Game.LOW_Y
                    self.pile_mat_list.append(pile)

                # Create the three set comparison piles
                # indexes 14-16
                for i in range(3):
                    pile = arcade.SpriteSolidColor(Game.MAT_WIDTH, Game.MAT_HEIGHT, arcade.color.GREEN_YELLOW)
                    pile.position = Game.SECONDARY_START_X + i * Game.X_SPACING, Game.COMPARISON_Y
                    self.pile_mat_list.append(pile)

                # Create the pile for other players' cards or set count
                # index 17
                pile = arcade.SpriteSolidColor(Game.MAT_WIDTH, Game.MAT_HEIGHT, arcade.color.GREEN_YELLOW)
                pile.position = Game.OTHER_PLAYER_START_X, Game.BOTTOM_Y
                self.pile_mat_list.append(pile)


                # Spritelist with all cards no matter where they are
                self.card_list = arcade.SpriteList()

                # Create all of the cards
                for color in Game.CARD_COLOR:
                    for shape in Game.CARD_SHAPE:
                        for filling in Game.CARD_FILLING:
                            for number in Game.CARD_NUMBER:
                                card = Game.Card(color, shape, filling, number, Game.CARD_SCALE)
                                card.position = Game.START_X, Game.BOTTOM_Y
                                self.card_list.append(card)
                
                # Shuffle the cards
                for position_1 in range(len(self.card_list)):
                    position_2 = randrange(len(self.card_list))
                    self.card_list[position_1], self.card_list[position_2] = self.card_list[position_2], self.card_list[position_1]
                
                for card in self.card_list:
                    # Create face down pile
                    card.face_down()
                    self.piles[0].append(card)

                # Deal deck
                for pile in range(2, 14):
                    # Get the top card from the face down deck
                    if len(self.piles[pile]) < 1:
                        card = self.piles[0].pop()
                        card.pile_number = pile
                        card.face_up()
                        self.piles[pile].append(card)
                        card.position = self.pile_mat_list[pile].position
                        self.pull_to_top(card)
                
                



        def on_draw(self):
            # Clear the screen
            arcade.start_render()
            
            # Draw the mats where the cards will go
            self.pile_mat_list.draw()
            
            # Draw the cards
            self.card_list.draw()

            arcade.draw_text(f"You have {self.set_count} set(s).", Game.START_X - 50, Game.BOTTOM_Y + Game.MAT_HEIGHT, arcade.color.WHITE, font_size=30)

            
            # Draw the score for each player
            if len(Game.player_dict) > 0:
                counter = 0
                for username in Game.player_dict:
                    counter += 1
                    # Font size of 30 is good for 10-12 charachters in the username
                    arcade.draw_text(f"{username} : {Game.player_dict[username]}", start_x=Game.SCREEN_WIDTH/1.25, start_y=Game.SCREEN_HEIGHT-100+(counter * 30), color=arcade.color.WHITE, font_size=30)  # - len(username))
            else:
                print("Dictionary is empty")

        

        def pull_to_top(self, card):
            """Pull card to top of rendering order (last to render, looks on top)"""
            # Find the index of the card
            index = self.card_list.index(card)
            # Loop and pull all the other cards down towards the zero end
            for i in range(index, len(self.card_list) - 1):
                self.card_list[i] = self.card_list[i+1]
            # Put this card at the right side/top/size of list
            self.card_list[-1] = card

        
        def on_key_press(self, symbol: int, modifiers: int):
            # Restart game
            if symbol == arcade.key.R:
                self.setup()



        def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
            # get list of cards (should be just 1) clicked on
            cards = arcade.get_sprites_at_point((x, y), self.card_list)
            # If a card was clicked on, select it
            if len(cards) > 0:
                # Get the card at clicked position
                selected_card = cards[-1]
                if not selected_card.is_face_down():
                    self.choose_card(selected_card)
                else:
                    print("This is a face down card. You cannot select that.")


        def choose_card(self, card):
            # Check for if the card has already been selected 
            if card not in self.selected_cards:
                self.selected_cards.append(card)
                self.selected_cards[-1].original_position = [self.selected_cards[-1].position]
                # Move card to first open comparison slot
                for pile in range(14, 17):
                    if len(self.piles[pile]) < 1:
                        card.original_position = card.position
                        card.position = self.pile_mat_list[pile].position
                        self.piles[pile].append(card)
                        card.comparison_pile_number = pile
                        break
            else:
                    card.position = card.original_position
                    self.piles[card.comparison_pile_number].pop()
                    self.selected_cards.remove(card)

            if len(self.selected_cards) >= 3:
                # Check for set
                if self.is_set(self.selected_cards[0], self.selected_cards[1], self.selected_cards[2]):
                    # If it is a set, remove the cards from the deck, uptick this players score, and package the object to be sent to server making sure the field is dealt to first.
                    # Then trigger the send function. This will be an instance, so the function call might need to import the send function from the networking client or server.
                    self.set_count += 1
                    for card in self.selected_cards:
                        card.is_face_up = False
                        card.position = self.pile_mat_list[1].position
                        self.piles[card.pile_number].pop()
                        self.piles[card.comparison_pile_number].pop()
                        self.pull_to_top(card)
                    self.selected_cards.clear()

                    for pile in range(2, 14):
                        # Deal a card to each open mat
                        if len(self.piles[pile]) < 1:
                            card = self.piles[0].pop()
                            card.face_up()
                            self.piles[pile].append(card)
                            card.pile_number = pile
                            card.position = self.pile_mat_list[pile].position
                            self.pull_to_top(card)
                    
                    Game.player_dict[self.username] += 1
                    Game.send_flag = True

                else:
                    for card in self.selected_cards:
                        # Remove card from the comparison slot
                        card.position = card.original_position
                        if card.pile_number is None:
                            card.pile_number = [self.pile_mat_list.index(card)]
                        self.piles[card.comparison_pile_number].pop()
                    # Clear the selected cards
                    self.selected_cards.clear()
                
        
        def is_set(self, card1, card2, card3):
            # use index to find the value of each aspect (like color, shape, or filling)
            aspect_1 = (Game.CARD_COLOR.index(card1.ccolor)+1) + (Game.CARD_COLOR.index(card2.ccolor)+1) + (Game.CARD_COLOR.index(card3.ccolor)+1)    
            aspect_2 = (Game.CARD_SHAPE.index(card1.shape)+1) + (Game.CARD_SHAPE.index(card2.shape)+1) + (Game.CARD_SHAPE.index(card3.shape)+1)
            aspect_3 = (Game.CARD_FILLING.index(card1.filling)+1) + (Game.CARD_FILLING.index(card2.filling)+1) + (Game.CARD_FILLING.index(card3.filling)+1)
            aspect_4 = (Game.CARD_NUMBER.index(card1.number)+1) + (Game.CARD_NUMBER.index(card2.number)+1) + (Game.CARD_NUMBER.index(card3.number)+1)
            if (aspect_1 == 3 or aspect_1 == 6 or aspect_1 == 9) and \
            (aspect_2 == 3 or aspect_2 == 6 or aspect_2 == 9) and \
            (aspect_3 == 3 or aspect_3 == 6 or aspect_3 == 9) and \
            (aspect_4 == 3 or aspect_4 == 6 or aspect_4 == 9):
                print("This is a set")
                return True
            else:
                print("This is not a set")
                return False


    class Card(arcade.Sprite):
        def __init__(self, color, shape, filling, number, scale=1):
            self.ccolor = color
            self.shape = shape
            self.filling = filling
            self.number = number
            self.original_position = None
            self.pile_number = None
            self.comparison_pile_number = None

            # Image to use for Card when face up
            # Images used from Geek and Sundry (https://geekandsundry.com/the-card-game-that-puzzled-mathematicians-for-decades/)
            self.image_file_name = f"images/{self.ccolor} {self.shape} {self.filling} {self.number}.png"
            self.is_face_up = False
            super().__init__(self.image_file_name, scale, hit_box_algorithm="None")

        def face_down(self):
            # Turn card face down
            self.texture = arcade.load_texture(Game.FACE_DOWN_IMAGE)
            self.is_face_up = False

        def face_up(self):
            # Turn card face up
            self.texture = arcade.load_texture(self.image_file_name)
            self.is_face_up = True
        
        def is_face_down(self):
            # check if the cardis face down
            return not self.is_face_up


def main():
    game = Game()
    my_window = game.Display()
    my_window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
