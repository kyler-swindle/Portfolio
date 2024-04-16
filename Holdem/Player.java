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

import java.util.ArrayList; // ArrayList Class, used for storing the pocket cards. 

// the Player Class is used for creating instances, referred to as 'Player-Objects,' 
// which are unique to each individual player
class Player {
   
   /**************************************************************************************************************** 
      Attributes: 
   */
   
   private ArrayList<Integer> pocket;  // ArrayList to store the two cards
                                       // that are dealt to each player.
   
   private boolean isIn; // ------------- boolean to determine whether the player will
                                       // stay 'in' (continue to play out) that
                                       // specific 'hand' (round with those cards) or 
                                       // 'fold' (quit that specific hand) instead. 
   
   private int hand; // ----------------- integer value, 0 - 10, each value of which refers to a
                                       // specific 'hand' [repeated term, but different meaning--
                                       // in this case, meaning a certain set of cards each player has, 
                                       // which includes those on the table (shared cards) and those
                                       // in their pocket], as denoted below:
                                          // 0 : No cards yet.
                                          // 1 : High Card - the card among the players with the highest rank.
                                          // 2 : Pair - two cards of the same rank.
                                          // 3 : Two-Pair - two Pairs of cards, each with unique ranks.
                                          // 4 : Three of a Kind - three cards of the same rank.
                                          // 5 : Straight - five cards of consecutive rank, disregarding suit 
                                             // (e.g. a five-high straight: "Ace, One, Two, Three, Four" 
                                             // on the low end, aka a 'baby straight,' 
                                             // or an ace-high straight: "Ten, Jack, Queen, King, Ace"
                                             // on the high end, aka a 'Broadway Straight.')
                                          // 6 : Flush - five cards of the same suit, disregarding rank.
                                          // 7 : Full House - a pair and a three of a kind.
                                          // 8 : Four of a Kind - four cards of the same rank.
                                          // 9 : Straight-Flush - five cards of consecutive rank with the same suit.
                                          // 10 : Royal Flush - an ace-high Straight-Flush.
   
   private int reserves; // ------------- integer to store the amount of money (Dollars, $) 
                                       // each player has.
   
   private int bet; // ------------------ integer to store the amount of funds each Player has bet, and/or, 
                                       // alternatively, if it is not yet their turn, their outstanding bet
                                       // prior to making the decision to match, raise, or fold another Player's
                                       // bet amount.
      
   /****************************************************************************************************************
      Constructor(s): 
   */
   
   // Player constructor to create new Player-Objects, 
   // initilizing each attribute with default values.
   Player () {
      this.hand = 0;
      this.reserves = 10000;
      this.isIn = true;
      this.pocket = new ArrayList<Integer>();
      this.bet = 0;
   }
   
   /****************************************************************************************************************
      Setter(s) & Getter(s): 
   */
   
   // getPlayer() outputs all of the private attributes 
   // in the Player Class.
   public void getPlayer () {
      System.out.println(this.hand);
      System.out.println(this.reserves);
      System.out.println(this.isIn);
      System.out.println(this.pocket);
      System.out.println(this.bet);
   }
   
   // getReserves() outputs the integer value of the 
   // respective Player's reserves.
   public int getReserves () {
      return this.reserves;
   }
   
   // setReserves() accesses the private int reserves to be 
   // used for removing or adding funds based on loss or win
   // of a hand (round).
   public void setReserves (int in) {
      this.reserves += in;
   }
   
   // getHand() outputs the integer value of the 
   // respective Player's current hand (set of cards).
   public int getHand () {
      return this.hand;
   }
   
   // setHand() access the private int hand to be used for 
   // setting the specific hand (set of cards) of the respective Player.
   public void setHand (int hand) {
      this.hand = hand;
   }
   
   // getPocket() outputs the private ArrayList<Integer> pocket, 
   // unique to each respective Player. 
   public ArrayList<Integer> getPocket () {
      return this.pocket;
   }
   
   // setPocket() accesses the private ArrayList<Integer> pocket, 
   // unique to each respective Player, to be used in the Table 
   // constructor when the cards are initially dealt to each Player.
   public void setPocket (ArrayList<Integer> cards) {
      this.pocket = cards;
   }
   
   // getBet() returns the private int bet, unique to each 
   // respective Player. 
   public int getBet () {
      return this.bet;
   }
   
   // setBet() accesses the private int bet, unique to each respective
   // Player, used in adding funds to the 'pot' of all other player's
   // bets and setting bet = 0 after doing so. 
   public void setBet (int bet) {
      this.bet = bet;
   }
   
   // getIsIn() returns the private boolean isIn, unique to each 
   // respective Player. 
   public boolean getIsIn () {
      return this.isIn;
   }
   
   // setIsIn() assigns the private boolean isIn, unique to each 
   // respective Player, used in determining whether the PLayer 
   // matches or folds. 
   public void setIsIn (boolean act) {
      this.isIn = act;
   }
   
   /****************************************************************************************************************
      Various methods(s): 
   */
   
   // comparePocket() method will compare the Player's pocket to the input
   // Player's pocket, assigning integer values to the ranks of each SIMP's
   // cards to determine who has the highest card of the two, if they have 
   // one of the same cards, then the 
   public int comparePocket (Player plr) {
      return -1; 
   }
   
   // betAmount() method determines the amount for each 'simulated' 
   // (to refrain from the use of the term 'A.I.') player, henceforth referred 
   // to as a "SIMP," to bet, weighing factors such as the following to make decisions: 
      // the respective SIMP's current hand, 
      // the amount that the respective SIMP has bet, 
         // compared to the amount in their reserves, 
      // the amount that the respective SIMP has bet, 
         // compared to the amount in the pot, 
      // the possibility of other player's having a higher hand than 
         // their own, based on the shared cards, 
      // and the probability that the SIMP can make a higher hand with
         // the outstanding shared cards to be dealt (if there are no 
         // more cards to be dealt, then, of course, that probability
         // would be zero), 
   public int betAmount () {
      /*
         WORK IN PROGRESS
            * currently only bets based on the SIMP's current hand & bet compared to reserves
      */
      
      if (this.hand <= 3) {
         setIsIn(true);
         // case for other SIMP's going all-in
         if (getBet() >= getReserves() || this.hand <= 5) { 
            setBet(getReserves());
            return getBet();
         } 
         // case for if the outstanding bet is lower 
         // than 33% of the SIMP's reserves
         if (getBet() <= (getReserves() / 3)) {
            setBet(getReserves() * 3);
            return getBet();
         }
         // defaults to 10% of reserves
         setBet(getReserves() / 10);
         return getBet();
      } else {
         setIsIn(false);
         setBet(0);
         return getBet();
      }
   }
}
