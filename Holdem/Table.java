/***** 
   Texas Hold'em Project 
   
   Date Started : Friday, April 12, 2024
   
   Date Finished : xxxday, XXX XX, XXXX
   
   Made by : Kyler A. Swindle (Auburn University - Software Engineering Major - Sophomore)
      Contact : 
         personal email: kswindle6544@gmail.com (PREFERRED),
         personal mobile: 256 - 224 - 5424 (text), 
         school email: kas0183@auburn.edu.
         
   Includes the following files: 
      * 'Game.java'
      * 'Table.java'
      * 'Player.java'

*/

import java.lang.Math; // ---- Math Class used for various arithmetic.

import java.util.Random; // -- Random Class used for generating random integers, 
                           // predominantly used in dealing cards, each assigned with
                           // a respective integer value, detailed below. 
                           // (see decodeCard() method for each specific value).

import java.util.ArrayList; // ArrayList Class used for various ArrayLists in both 
                            // the Player Class and this Class.

// the Table Class handles the majority of the game content, 
// assigning random cards dealing the cards to each of the Players, 
// and dealing the flop, turn, and river cards (aka 'shared cards').
class Table {
   
   /****************************************************************************************************************
      Attributes(s): 
   */
   
   public ArrayList<Integer> allCards; // stores all of the dealt cards, 
                                       // including those on the table, and 
                                       // each of the player's pocket cards (2 each),
                                       
   public ArrayList<Integer> table; // -- stores the cards on the table, 
                                       // including the flop (the first 3 shared cards), 
                                       // turn (the 4th shared card, 
                                       // and the river (the 5th and final shared card).
   
   public ArrayList<Player> players;// -- stores each of the players in the game as a 
                                       // Player-Object. 
                                       // (See 'Player.Java' for more info).
   
   /****************************************************************************************************************
      Constructor(s): 
   */
   
   // Table constructor takes the number of players as input, 
   // initilizes each of the ArrayLists allCards, table, and players.
   // Then, it adds new Player-Objects based on the number of input
   // players, assigning each one two newCards, and adding them to
   // the ArrayList allCards, and the Pocket-ArrayList unique to each
   // Player-Object.
   Table (int numPlayers) {
      // ArrayList initilization
      this.allCards = new ArrayList<Integer>();
      this.table = new ArrayList<Integer>();
      this.players = new ArrayList<Player>();
      
      // Loop to create new Player-Objects for each of those specified
      // by the constructor input.
      for (int i = 0; i < numPlayers; i++) {
         this.players.add(new Player()); // adds new Player-Object to the players ArrayList
         
         // Nested loop to add the cards (integers) to the ArrayList allcards, 
         // and the ArrayList pocket, specific to each Player.
         for (int j = 0; j < 2; j++) {
            int card = newCard();
            
            this.allCards.add(card);
            this.players.get(i).setPocket(card); 
         }
      }
   }
   
   /****************************************************************************************************************
      Various methods(s): 
   */
   
   // newCard() creates a random number, checking it against the 
   // values that are already in the allCards ArrayList to 
   // prevent duplicates.
   public int newCard () {
      Random rnd = new Random();
      int card = rnd.nextInt(52) + 1;
      while (this.allCards.contains(card)) {
         card = rnd.nextInt(52) + 1;
      }
      return card;
   }
   
   // decodeCard() outputs the string representation of the assigned integer card value,
   // using a StringBuilder.
      // First block of if's determines the rank,
      // Second if-block assigns the suit.
   public String decodeCard (int card) {
      StringBuilder sb = new StringBuilder();
      
      // Rank of the card (i.e. 2 - 10, Jack, Queen, King, Ace).
      if (card == 1 || card == 14 || card == 27 || card == 40) {
         sb.append("Two");
      } else if (card == 2 || card == 15 || card == 28 || card == 41) {
         sb.append("Three");
      } else if (card == 3 || card == 16 || card == 29 || card == 42) {
         sb.append("Four");
      } else if (card == 4 || card == 17 || card == 30 || card == 43) {
         sb.append("Five");
      } else if (card == 5 || card == 18 || card == 31 || card == 44) {
         sb.append("Six");
      } else if (card == 6 || card == 19 || card == 32 || card == 45) {
         sb.append("Seven");
      } else if (card == 7 || card == 20 || card == 33 || card == 46) {
         sb.append("Eight");
      } else if (card == 8 || card == 21 || card == 34 || card == 47) {
         sb.append("Nine");
      } else if (card == 9 || card == 22 || card == 35 || card == 48) {
         sb.append("Ten");
      } else if (card == 10 || card == 23 || card == 36 || card == 49) {
         sb.append("Jack");
      } else if (card == 11 || card == 24 || card == 37 || card == 50) {
         sb.append("Queen");
      } else if (card == 12 || card == 25 || card == 38 || card == 51) {
         sb.append("King");
      } else {
         sb.append("Ace");
      }
      
      // Suit of the card (i.e. Hearts, Diamonds, Spades, or Clubs).
      if (card <= 13) {
         sb.append(" of Hearts");
      } else if (card <= 26) {
         sb.append(" of Diamonds");
      } else if (card <= 39) {
         sb.append(" of Spades");
      } else {
         sb.append(" of Clubs");
      }
      
      return sb.toString();
   }
   
}