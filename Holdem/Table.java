/***** 
   Texas Hold'em Project 
   
   Date Started : Friday, April 12, 2024, 19:15
   
   Date Finished : xxxday, XXX XX, XXXX, XX:XX
   
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

import java.lang.Math; // ------ Math Class used for various arithmetic.

import java.util.Random; // ---- Random Class used for generating random integers, 
                              // predominantly used in dealing cards, each assigned with
                              // a respective integer value, detailed below. 
                              // (see decodeCard() method for each specific value).

import java.util.ArrayList; // - ArrayList Class used for various ArrayLists in both 
                              // the Player Class and this Class.

import java.util.HashSet; // --- HashSet Class for removing duplicates from certain
                              // ArrayLists. 
                              
import java.util.Set; // ------- Set Interface to implement the HashSet Class. 

import java.util.Collections; // Collections Class used for the .frequency() method.

// the Table Class handles the majority of the game content, 
// assigning random cards dealing the cards to each of the Players, 
// dealing the flop cards, turn card, and river card (aka 'shared cards'), 
// the betting system, checking each of the Players' hands, etc.
class Table {
   
   /****************************************************************************************************************
      Attributes(s): 
   */
   
   public ArrayList<Integer> allCards; // stores all of the dealt cards, 
                                       // including those on the table, and 
                                       // each of the player's pocket cards (2 each).
                                       
   public ArrayList<Integer> table; // -- stores the cards on the table, 
                                       // including the flop (the first 3 shared cards), 
                                       // turn (the 4th shared card, 
                                       // and the river (the 5th and final shared card).
   
   public ArrayList<Player> players;// -- stores each of the players in the game as a 
                                       // Player-Object. 
                                       // (See 'Player.Java' for more info).
   
   public ArrayList<Player> folded; // -- stores each of the players in the game, who have
                                       // folded, so they can be added back for the next hand. 
   
   public int pot; // ------------------- stores the integer value of the current sum of funds
                                       // that have been bet by each of the Players.
   
   public int currTurn; // -------------- stores the integer value of the index of the player
                                       // whose turn it currently is, specifically for use in
                                       // the fold() and nextPlayer() methods.
                                       // (See fold() and nextPlayer() methods for more info).
   
   public ArrayList<Player> tied; //----- stores each of the players in the game, who have tied
                                       // their hands, so that the pot may be split between them.
   
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
      // ArrayList & attribute initilization
      this.allCards = new ArrayList<Integer>();
      this.table = new ArrayList<Integer>();
      this.players = new ArrayList<Player>();
      this.folded = new ArrayList<Player>();
      this.tied = new ArrayList<Player>();
      this.pot = 0;
      this.currTurn = 0;
      
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
   // values that are already in the allCards ArrayList and adding 
   // the newCard integer to the allCards ArrayList prior to 
   // returning the value, in order to prevent duplicates.
   public int newCard () {
      Random rnd = new Random();
      int card = rnd.nextInt(52) + 1;
      while (this.allCards.contains(card)) {
         card = rnd.nextInt(52) + 1;
      }
      this.allCards.add(card);
      return card;
   }
   
   // flop() method deals the flop, 
   // assigning 3 cards to the table ArrayList. 
   public void flop () { 
      for (int i = 0; i < 3; i++) {
         int card = newCard();
         
         this.table.add(card);
      }
      
      postCard();
   }
   
   // turn() method deals the turn, assigning 1 additional 
   // card to make a total of 4 shared cards in the table ArrayList.
   public void turn () {
      int card = newCard();
         
      this.table.add(card);
      
      postCard();
   }
   
   // river() method deals the river, assigning 1 additional 
   // card to make a total of 5 shared cards in the table ArrayList.
   public void river () {
      int card = newCard();
         
      this.table.add(card);
      
      postCard();
   }
   
   // postCard() method combines and calls all methods that are necessary 
   // after (an) additional shared card(s) are dealt.
   public void postCard () {
      if (this.currTurn >= this.players.size()) {
        this.currTurn = 0; 
      }
      for (Player P : this.players) {
         this.players.get(currTurn).setHand(checkHand());
         nextPlayer();
      }
   }
   
   // nextPlayer() method increments the currTurn integer and ensures
   // that it is a valid value (0 - [number of players]). 
   public void nextPlayer () {
      this.currTurn++; 
      if (this.currTurn > (this.players.size() - 1)) {
         this.currTurn = 0;
      }
      if (!this.players.get(this.currTurn).getIsIn()) {
         this.currTurn++;
      }
   }
   
   // EOH() method (stands for End of Hand) performs various actions 
   // after the hand (round) is over, such as: 
      // checking which Player has the winning hand, 
      // awarding the pot to the winning player, 
      // adding Players in ArrayList folded back to ArrayList players,
      // removing SIMPs from the ArrayList tied,
      // removing SIMPs that ran out of funds,
      // and ensuring all Players' in ArrayList players bets are set
         // back to zero. 
   public void EOH () {
      /* 
         WORK IN PROGRESS
            (note: perhaps separate the winning hand into another method...)
      */
   }
   
   // fold() method performs actions necessary for removing a Player 
   // from a hand (round). 
   public void fold () {
      
   }
   
   // bettingSequence() method iterates through each of the players 
   // to allow for each to bet, match, or fold. 
   public void bettingSequence () {
      while (!areBetsMatched()) {
         for (int i = 0; i < this.players.size(); i++) {
            this.players.get(i).setBet(this.players.get(i).betAmount());
            nextPlayer();
         }
      }
   }
   
   // areBetsMatched() method returns a boolean value to determine 
   // if there are any players who have not yet matched the bet of 
   // another player.
   public boolean areBetsMatched () {
      for (int i = 0; i < this.players.size(); i++) {
         for (int j = 0; j < this.players.size(); j++) {
            if (this.players.get(i).getBet() != this.players.get(j).getBet()) {
               return false;
            }
         }
      }
      return true;
   }
   
   // checkHand() method checks the pocket cards of individual Players, 
   // as well as the shared cards via the table ArrayList, in order to 
   // assign each respective SIMP with an integer value referring to the
   // hand that they currently have. Returns the hand as an int 0 - 10. 
   public int checkHand () {
      int hand = 0;
      if (this.currTurn >= this.players.size()) {
        this.currTurn = 0; 
      }
      ArrayList<Integer> combCards = new ArrayList<>(this.players.get(currTurn).getPocket());
      combCards.addAll(this.table);
      
      ArrayList<Integer> encCards = new ArrayList<>();
      for (Integer n : combCards ) {
         encCards.add(encodeRank(n));
      }
      Set<Integer> tempSet = new HashSet<>(encCards);
      ArrayList<Integer> remDups = new ArrayList<>(tempSet);
      
      // checks if the Player has the High Card among all the other dealt cards 
      int highCard = 0;
      for (int i = 0; i < this.allCards.size(); i++) {
         if (encodeRank(highCard) <= encodeRank(this.allCards.get(i))) {
            highCard = encodeRank(this.allCards.get(i));
         }
      }
      
      // sets hand for a High Card
      if (this.players.get(currTurn).getPocket().contains(highCard) || 
          this.players.get(currTurn).getPocket().contains(highCard + 13) ||
          this.players.get(currTurn).getPocket().contains(highCard + 26) ||
          this.players.get(currTurn).getPocket().contains(highCard + 39)) {
         hand = 1;
      }
      
      // checks for Pairs, Three of a Kind, and Four of a Kind, comparing 
      // ArrayLists encCards and remDups, the former of which is an ArrayList
      // of the rank-encoded values of each of the cards, and the latter 
      // is an ArrayList of the ranks without any duplicate values. 
      int numPairs = 0;
      int numTrios = 0;
      int numQuads = 0;
      int likeRanks = 0;
      for (Integer rank : remDups) {
         likeRanks = Collections.frequency(encCards, rank);
         if (likeRanks == 4) {
            numQuads++;
         } else if (likeRanks == 3) {
            numTrios++;
         } else if (likeRanks == 2) {
            numPairs++;
         }
      }
      
      // sets for hand for a Pair
      if (numPairs == 1) {
         hand = 2;
      }
      
      // sets hand for Two-Pair ****NEEDS TO BE FIXED****
      if (numPairs == 2) {
         hand = 3;
      }
      
      // sets hand for a Three of a Kind
      if (numTrios == 1) {
         hand = 4;
      }
      
      // checks for a straight among the ArrayList sortedRanks, which
      // has also had any duplicates removed via temporarily converting
      // it to a HashSet.  
      boolean straight = false; 
      ArrayList<Integer> sortedRanks = new ArrayList<>(remDups);
      Collections.sort(sortedRanks);
      
      int consecutive = 1;
      for (int i = 0; i < sortedRanks.size() - 1; i++) {
         if (sortedRanks.get(i) == sortedRanks.get(i + 1) - 1) {
            consecutive++;
         } else {
            consecutive = 1;
         }
      }
      
      if (consecutive >= 5) {
         straight = true;
      }
            
      // checks for flush among combCards
      boolean flush = false;
      int numHearts = 0;
      int numDiamonds = 0;
      int numSpades = 0;
      int numClubs = 0;
            
      for (int i = 0; i < combCards.size(); i++) {
         if (combCards.get(i) <= 13) {
            numHearts++;
         } else if (combCards.get(i) <= 26) {
            numDiamonds++;
         } else if (combCards.get(i) <= 39) {
            numSpades++;
         } else {
            numClubs++;
         }
      }
      
      // sets Hand for a Flush
      if (numHearts >= 5 || numDiamonds >= 5 || numSpades >= 5 || numClubs >= 5) {
         flush = true;
         hand = 6;
      }
      
      // sets Hand for a Full House
      if (numTrios == 1 && numPairs == 1) {
         hand = 7;
      }
      
      // sets Hand for a Four of a Kind
      if (numQuads == 1) {
         hand = 8;
      }
      
      // checks for a Straight-Flush among the sorted combCards
      ArrayList<Integer> sortedComb = new ArrayList<>(combCards);
      Collections.sort(sortedComb);
      int consecutiveSuited = 1;
      for (int i = 0; i < sortedComb.size() - 1; i++) {
         if (consecutiveSuited >= 5) {
            break;
         }
         int curr = sortedComb.get(i); 
         int next = sortedComb.get(i + 1);
         if ((curr == next - 1) && !(curr == 10 || curr == 11 || curr == 12 || curr == 13 ||
                                    curr == 23 || curr == 24 || curr == 25 || curr == 26 ||
                                    curr == 36 || curr == 37 || curr == 38 || curr == 39 || 
                                    curr == 49 || curr == 50 || curr == 51 || curr == 52)) {
            consecutiveSuited++;
            if (consecutiveSuited >= 5) {
               break;
            }
         } else {
            if (consecutiveSuited >= 5) {
               break;
            }
            consecutiveSuited = 1;
         }
      }      
      
      // sets Hand for a Straight-Flush
      if (consecutiveSuited >= 5) {
         hand = 9;
      }
      
      // sets hand for a Royal Flush, checking the cards directly
      if ((combCards.contains(13) && combCards.contains(12) && combCards.contains(11) && combCards.contains(10) && combCards.contains(9)) || 
         (combCards.contains(26) && combCards.contains(25) && combCards.contains(24) && combCards.contains(23) && combCards.contains(22)) || 
         (combCards.contains(39) && combCards.contains(38) && combCards.contains(37) && combCards.contains(36) && combCards.contains(35)) || 
         (combCards.contains(52) && combCards.contains(51) && combCards.contains(50) && combCards.contains(49) && combCards.contains(48))) {
         hand = 10;
      }
      
      return hand;
   }
   
   // currHighestHand() method returns the index of the player with the 
   // current highest hand, checking for the highest value among each 
   // of the SIMP's private hand variables.
   public int currHighestHand () {
      int highIndex = 0; // the index of the SIMP with the highest hand
      
      // Iterates each of the SIMPs in players ArrayList to determine
      // which one has the highest hand private variable. 
      for (int i = 0; i < this.players.size(); i++) {         
         if (this.players.get(i).getHand() >= this.players.get(highIndex).getHand()) {
            highIndex = i; // re-assigns highIndex to the SIMP with the highest hand
         }
      }
      
      return highIndex;
   }
   
   // encodeRank() method returns an integer value for the rank of each card
   // 2 (Two) - 14 (Ace). 
   public int encodeRank (int card) {
      if (card == 1 || card == 14 || card == 27 || card == 40) {
         return 2;
      } else if (card == 2 || card == 15 || card == 28 || card == 41) {
         return 3;
      } else if (card == 3 || card == 16 || card == 29 || card == 42) {
         return 4;
      } else if (card == 4 || card == 17 || card == 30 || card == 43) {
         return 5;
      } else if (card == 5 || card == 18 || card == 31 || card == 44) {
         return 6;
      } else if (card == 6 || card == 19 || card == 32 || card == 45) {
         return 7;
      } else if (card == 7 || card == 20 || card == 33 || card == 46) {
         return 8;
      } else if (card == 8 || card == 21 || card == 34 || card == 47) {
         return 9;
      } else if (card == 9 || card == 22 || card == 35 || card == 48) {
         return 10;
      } else if (card == 10 || card == 23 || card == 36 || card == 49) {
         return 11;
      } else if (card == 11 || card == 24 || card == 37 || card == 50) {
         return 12;
      } else if (card == 12 || card == 25 || card == 38 || card == 51) {
         return 13;
      } else {
         return 14;
      }
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
   
   // decodeHand() outputs the corresponding String representation of 
   // the integer value that stores the respective hand. 
   public String decodeHand (int hand) {
      if (hand == 1) {
         return "Pair";
      } else if (hand == 2) {
         return "Pair";
      } else if (hand == 3) {
         return "Two-Pair";
      } else if (hand == 4) {
         return "Three of a Kind";
      } else if (hand == 5) {
         return "Straight";
      } else if (hand == 6) {
         return "Flush";
      } else if (hand == 7) {
         return "Full House";
      } else if (hand == 8) {
         return "Four of a Kind";
      } else if (hand == 9) {
         return "Straight-Flush";
      } else if (hand == 10) {
         return "Royal Flush";
      } else {
         return "null";
      }
   }
   
}
