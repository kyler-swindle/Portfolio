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

import java.util.Iterator; // -- Iterator Interface used for simplyfing the removal of 
                              // elements from various ArrayLists. 

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

   public ArrayList<Player> tied; //----- stores each of the players in the game, who have tied
                                       // their hands, so that the pot may be split between them.
   
   public ArrayList<Player> folded; // -- stores each of the players in the game, who have
                                       // folded, so they can be added back for the next hand. 
   
   public int pot; // ------------------- stores the integer value of the current sum of funds
                                       // that have been bet by each of the Players.
   
   public int currTurn; // -------------- stores the integer value of the index of the player
                                       // whose turn it currently is, specifically for use in
                                       // the fold() and nextPlayer() methods.
                                       // (See fold() and nextPlayer() methods for more info).
   
   public int dealer; // ---------------- stores the index of the Player, who acts as the dealer, 
                                       // in that they are the last SIMP to 'act' after addtional
                                       // shared card(s) have been dealt, i.e. the first Player
                                       // to act, known as 'left-of-dealer,' will play the 'small
                                       // blind' (a small amount of money placed in the pot prior 
                                       // to recieving cards to ensure the pot is not empty), and 
                                       // the Player to the left of them plays the 'big blind' 
                                       // (twice the amount of the small blind). 
                                       
   public boolean flop; // -------------- stores whether the flop has been played yet in the 
                                       // current hand.
   
   public boolean turn; // -------------- stores whether the turn has been played yet in the 
                                       // current hand.
   
   public boolean river; // ------------- stores whether the river has been played yet in the 
                                       // current hand.
   
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
      this.dealer = 0;
      this.flop = false;
      this.turn = false;
      this.river = false;
      
      // Loop to create new Player-Objects for each of those specified
      // by the constructor input.
      for (int i = 0; i < numPlayers; i++) {
         this.players.add(new Player()); // adds new Player-Object to the players ArrayList
         
         ArrayList<Integer> playerCards = new ArrayList<Integer>();
         // Nested loop to add the cards (integers) to the ArrayList allCards, 
         // and the ArrayList pocket, specific to each Player.
         for (int j = 0; j < 2; j++) {
            int card = newCard();
            playerCards.add(card);
            this.allCards.add(card); 
         }
         this.players.get(i).setPocket(playerCards);
      }
   }
   
   
   /****************************************************************************************************************
      Various methods(s): 
   */
   
   // newCard() generates a random number, checking it against the 
   // values that are already in the allCards ArrayList and adding 
   // the newCard integer to the allCards ArrayList prior to 
   // returning the value, in order to prevent duplicates.
   public int newCard () {
      Random rnd = new Random();
      int card = rnd.nextInt(52);
      while (this.allCards.contains(card)) {
         card = rnd.nextInt(52);
      }
      this.allCards.add(card);
      return card;
   }
   
   // removePlayer() removes the Player-Object specied by parameter ind from all local 
   // ArrayLists and their cards from the allCards ArrayList.
   public void removePlayer (int ind) {
      // temporary ArrayList to store the SIMP's pocket cards so they can 
      // be removed from allCards ArrayList
      ArrayList<Integer> cardsToRem = new ArrayList<>();
      for (int i = 0; i < 2; i++) {
         cardsToRem.add(this.players.get(ind).getPocket().get(i));
      }
      
      for (int i = this.allCards.size() - 1; i >= 0; i--) {
         if (this.players.get(ind).getPocket().contains(this.allCards.get(i))) {
            this.allCards.remove(i); // removes SIMP's pocket cards from allCards
         }
      }
      
      // removes the respective Player-Object from both ArrayLists tied and folded.
      Iterator<Player> foldedItr = this.folded.iterator();
      while (foldedItr.hasNext()) {
         Player plr = foldedItr.next();
         if (plr.equals(this.players.get(ind))) {
            foldedItr.remove();
         }
      }
      Iterator<Player> tiedItr = this.tied.iterator();
      while (tiedItr.hasNext()) {
         Player plr = tiedItr.next();
         if (plr.equals(this.players.get(ind))) {
            tiedItr.remove();
         }
      } 
      
      this.players.remove(ind);
      nextPlayer();
   }
   
   // removePlayers() method uses recursion to remove players based on the 
   // inputted indices of those passed through the method call. 
   public int removePlayers (ArrayList<Integer> indices) {
      if (indices.isEmpty()) {
         return 0; // returns 0 if no indices of SIMPs could be found to remove
      }
      
      removePlayer(indices.get(0)); // -- Removes the Player that corresponds to index of the first 
                                       // element that is in ArrayList indices in each recursive call. 
      indices.remove(0); // ------------- Removes the integer index from ArrayList indices that was 
                                       // used to remove the Player corresponding to that integer.
      
      for (int n = 0; n < indices.size(); n++) {
         indices.set(n, indices.get(n) - 1); // Decrements each element of ArrayList indices to account 
                                             // for the decreased size of the ArrayList players after 
                                             // removePlayer() is called.
      }
            
      return removePlayers(indices) + 1; // Recursively calls removePlayers() and returns the number of 
                                          // Players that were removed. 
   }
   
   // flop() method deals the flop, 
   // assigning 3 cards to the table ArrayList. 
   public void flop () { 
      this.flop = true;
      
      for (int i = 0; i < 3; i++) {
         int card = newCard();
         this.table.add(card);
      }
      
      postCard();
   }
   
   // turn() method deals the turn, assigning 1 additional 
   // card to make a total of 4 shared cards in the table ArrayList.
   public void turn () {
      this.turn = true;
      
      int card = newCard();
      this.table.add(card);
      
      postCard();
   }
   
   // river() method deals the river, assigning 1 additional 
   // card to make a total of 5 shared cards in the table ArrayList.
   public void river () {
      this.river = true;
      
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
         P.setHand(checkHand());
         nextPlayer();
      }
   }
   
   // nextPlayer() method increments the currTurn integer and ensures
   // that it is a valid value (0 - [number of players - 1]). 
   public void nextPlayer () {
      if (this.players.isEmpty()) {
         return;
      }
      
      this.currTurn++; 
      if (this.currTurn >= this.players.size()) {
         this.currTurn = 0;
      }
      while (!this.players.get(this.currTurn).getIsIn()) {
         this.currTurn++;
         if (this.currTurn >= this.players.size()) {
            this.currTurn = 0;
         }
      }
   }
   
   // nextDealer() method increments the dealer integer and ensures
   // that it is a valid value (0 - [number of players - 1]). 
   public void nextDealer () {
      if (this.players.isEmpty()) {
         return;
      }
      
      this.dealer++; 
      if (this.dealer >= this.players.size()) {
         this.dealer = 0;
      }
      while (!this.players.get(this.dealer).getIsIn()) {
         this.dealer++;
         if (this.dealer >= this.players.size()) {
            this.dealer = 0;
         }
      }
   }
   
   // leftOfDealer() method returns the index of the player who is 
   // currently to the left of the dealer.
   public int leftOfDealer () {      
      if (this.players.isEmpty()) {
         return -1;
      }
      
      int LOD = this.dealer + 1;
      
      if (LOD >= this.players.size()) {
         if (!this.players.get(0).getIsIn()) {
            return leftOfDealer();
         } else {                                                       /****** i dont think i need this? ******/
            return 0;
         }
      }
      
      while (!this.players.get(this.currTurn).getIsIn()) {
         this.currTurn++;
         if (this.currTurn >= this.players.size()) {
            this.currTurn = 0;
         }
      }
      
      return LOD;
   }
   
   // resetPlayers() method resets each player to their default attribute
   // states (excluding reserves).
   public void resetPlayers() {
      for (Player p : this.players) {
         p.setIsIn(true);
         p.setBet(0);
         p.setHand(0);
         p.setPocket(new ArrayList<Integer>());
      }
   }
   
   // resetHands() method resets each Player's hand zero.
   public void resetHands() {
      for (Player p : this.players) {
         p.setHand(0);
      }
   }
   
   // endOfHand() method performs various actions after the hand (round)
   // is over, such as: 
      // checking which Player has the winning hand, 
      // awarding the pot to the winning player, 
      // adding Players in ArrayList folded back to ArrayList players,
      // removing SIMPs from the ArrayList tied,
      // removing SIMPs that ran out of funds,
      // and ensuring all Players' in ArrayList players bets are set
         // back to zero. 
   public void endOfHand () {
      /* 
         WORK IN PROGRESS
            (note: perhaps separate the winning hand into another method...)
      */
   }
   
   // fold() method performs actions necessary for removing a Player 
   // from a hand (round). 
   public void fold () {
      /*
         im wondering if this is even necessary?
         cause all it would do is add Players to folded Arraylist 
         or remove them from players ArrayList, which would be 
         redundant since isIn is already a parameter?
      */
   }
   
   // bettingSequence() method iterates through each of the players 
   // to allow for each to bet, match, or fold. 
   public void bettingSequence () {
      while (!areBetsMatched()) {
         this.players.get(this.currTurn).setBet(this.players.get(this.currTurn).betAmount());
         if (this.players.get(this.currTurn).getIsIn()) {
            this.pot += this.players.get(this.currTurn).getBet();
         } else {
            fold();
         }
         nextPlayer();
      }
   }
   
   // areBetsMatched() method returns a boolean value to determine 
   // if there are any players who have not yet matched the bet of 
   // another player.
   public boolean areBetsMatched () {
      for (int i = 0; i < this.players.size(); i++) {
         for (int j = 0; j < this.players.size(); j++) {
            if (this.players.get(i).getIsIn() && this.players.get(j).getIsIn()) {
               if (this.players.get(i).getBet() != this.players.get(j).getBet()) {
                  return false;
               }
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
      int hand = this.players.get(this.currTurn).getHand();
      if (this.currTurn >= this.players.size()) {
        this.currTurn = 0; 
      }
      ArrayList<Integer> tempComb = new ArrayList<>(this.players.get(this.currTurn).getPocket());
      tempComb.addAll(this.table);
      ArrayList<Integer> combCards = new ArrayList<>(tempComb);
      
      ArrayList<Integer> rankCards = new ArrayList<>();
      for (Integer n : combCards ) {
         rankCards.add(n / 4);
      }
      Set<Integer> tempSet = new HashSet<>(rankCards);
      ArrayList<Integer> remDups = new ArrayList<>(tempSet);
      
      // checks if the Player has the High Card among rankCards 
      int highCard = 0;
      for (Integer X : rankCards) {
         if (X > highCard) {
            highCard = X;
         }
      }
      
      // sets hand for a High Card
      if (rankCards.contains(highCard)) {
         if (this.players.get(this.currTurn).getHand() <= 1) {
            hand = 1;
         }
      }
      
      // checks for Pairs, Three of a Kind, and Four of a Kind, comparing 
      // ArrayLists encCards and remDups, the former of which is an ArrayList
      // of the rank-encoded values of each of the cards, and the latter 
      // is an ArrayList of the ranks without any duplicate values. 
      int numPairs = 0;
      int numTrios = 0;
      int numQuads = 0;
      for (Integer rank : remDups) {
         int likeRanks = 0;
         for (Integer dup : rankCards) {
            if (rank == dup) {
               likeRanks++;
            }
         }
         
         if (likeRanks == 4) {
            numQuads++;
         } else if (likeRanks == 3) {
            numTrios++;
         } else if (likeRanks == 2) {
            numPairs++;
         }
      }
      
      // sets for hand for a Pair
      if (numPairs >= 1) {
         if (this.players.get(this.currTurn).getHand() < 2) {
            hand = 2;
         }
      }
      
      // sets hand for Two-Pair
      if (numPairs >= 2) {
         if (this.players.get(this.currTurn).getHand() < 3) {
            hand = 3;
         }
      }
      
      // sets hand for a Three of a Kind
      if (numTrios >= 1) {
         if (this.players.get(this.currTurn).getHand() < 4) {
            hand = 4;
         }
      }
      
      // checks for a straight among the ArrayList sortedRanks, which
      // has also had any duplicates removed via temporarily converting
      // it to a HashSet.  
      ArrayList<Integer> tempSorted = new ArrayList<>(remDups);
      Collections.sort(tempSorted);
      ArrayList<Integer> sortedRanks = new ArrayList<>(tempSorted);
      for (Integer x : tempSorted) {
         if (x == 0) {
            sortedRanks.add(13); // adds Aces as 13's as well for the case of a Broadway straight
         }
      }
      
      int consecutive = 1;
      for (int i = 0; i < sortedRanks.size() - 1; i++) {
         if (sortedRanks.get(i) == sortedRanks.get(i + 1) - 1) {
            consecutive++;
            if (consecutive >= 5) {
               break;
            }
         } else {
            consecutive = 1;
         }
      }
      
      if (consecutive >= 5) {
         if (this.players.get(this.currTurn).getHand() < 5) {
            hand = 5;
         }
      }
            
      // checks for flush among combCards
      int numHearts = 0;
      int numDiamonds = 0;
      int numSpades = 0;
      int numClubs = 0;
            
      for (int i = 0; i < combCards.size(); i++) {
         if (combCards.get(i) % 4 == 0) {
            numHearts++;
         } else if (combCards.get(i) % 4 == 1) {
            numDiamonds++;
         } else if (combCards.get(i) % 4 == 2) {
            numSpades++;
         } else {
            numClubs++;
         }
      }
      
      // sets Hand for a Flush
      if (numHearts >= 5 || numDiamonds >= 5 || numSpades >= 5 || numClubs >= 5) {
         if (this.players.get(this.currTurn).getHand() < 6) {
            hand = 6;
         }
      }
      
      // sets Hand for a Full House
      if (numTrios >= 1 && numPairs >= 1) {
         if (this.players.get(this.currTurn).getHand() < 7) {
            hand = 7;
         }
      }
      
      // sets Hand for a Four of a Kind
      if (numQuads >= 1) {
         if (this.players.get(this.currTurn).getHand() < 8) {
            hand = 8;
         }
      }
      
      
      // checks for a Straight-Flush among the sorted combCards by first
      // iterating and and checking cards for a specific suit to a separate 
      // temp ArrayList suitedCards, then it checks for consecuitives within 
      // suitedCards. 
      ArrayList<Integer> sortedComb = new ArrayList<>(combCards);
      Collections.sort(sortedComb);
      int consecutiveSuited = 1;
      for (int i = 0; i < 4; i++) {
         ArrayList<Integer> suitedRanks = new ArrayList<>();
         for (Integer x : sortedComb) {
            if (x % 4 == i) {
               if (x / 4 == 0) {
                  suitedRanks.add(13); // if an Ace is present, adds it as a 13 as well 
                  suitedRanks.add(x / 4); // as a 0 (zero)
               } else {
                  suitedRanks.add(x / 4); // otherwise adds rank as normal
               }
            }
         }
                  
         if (suitedRanks.size() >= 5) {
            for (int j = 0; j < suitedRanks.size() - 1; j++) {
               int curr = suitedRanks.get(j);
               int next = suitedRanks.get(j + 1);
               if (curr == next - 1) {
                  consecutiveSuited++;
                  if (consecutiveSuited >= 5) {
                     break;
                  }
               } else {
                  consecutiveSuited = 1;
               }
            }
         }
         
         if (consecutiveSuited >= 5) {
            break;
         } else {
            consecutiveSuited = 1;
         }
      }
            
      // sets Hand for a Straight-Flush
      if (consecutiveSuited >= 5) {
         if (this.players.get(this.currTurn).getHand() < 9) {
            hand = 9;
         }
      } 
      
      // sets hand for a Royal Flush, checking the cards directly
      if ((combCards.contains(0) && combCards.contains(36) && combCards.contains(40) && combCards.contains(44) && combCards.contains(48)) || 
         (combCards.contains(1) && combCards.contains(37) && combCards.contains(41) && combCards.contains(45) && combCards.contains(49)) || 
         (combCards.contains(2) && combCards.contains(38) && combCards.contains(42) && combCards.contains(46) && combCards.contains(50)) || 
         (combCards.contains(3) && combCards.contains(39) && combCards.contains(43) && combCards.contains(47) && combCards.contains(51))) {
         if (this.players.get(this.currTurn).getHand() < 10) {
            hand = 10;
         }
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
      
   // decodeCard() outputs the string representation of the assigned integer card value,
   // using a StringBuilder.
      // First block of if's determines the rank,
      // Second if-block assigns the suit.
   public String decodeCard (int card) {
      StringBuilder sb = new StringBuilder();
      
      // Rank of the card (i.e. Ace, 2 - 10, Jack, Queen, King).
      if (card / 4 == 0) {
         sb.append("Ace");
      } else if (card / 4 == 1) {
         sb.append("Two");
      } else if (card / 4 == 2) {
         sb.append("Three");
      } else if (card / 4 == 3) {
         sb.append("Four");
      } else if (card / 4 == 4) {
         sb.append("Five");
      } else if (card / 4 == 5) {
         sb.append("Six");
      } else if (card / 4 == 6) {
         sb.append("Seven");
      } else if (card / 4 == 7) {
         sb.append("Eight");
      } else if (card / 4 == 8) {
         sb.append("Nine");
      } else if (card / 4 == 9) {
         sb.append("Ten");
      } else if (card / 4 == 10) {
         sb.append("Jack");
      } else if (card / 4 == 11) {
         sb.append("Queen");
      } else {
         sb.append("King");
      }
      
      // Suit of the card (i.e. Hearts, Diamonds, Spades, or Clubs).
      if (card % 4 == 0) {
         sb.append(" of Hearts");
      } else if (card % 4 == 1) {
         sb.append(" of Diamonds");
      } else if (card % 4 == 2) {
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
         return "High Card";
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
