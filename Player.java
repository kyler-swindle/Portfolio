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
   
   /****************************************************************************************************************
      Constructor(s): 
   */
   
   // Player constructor to create new Player-Objects, 
   // initilizing each attribute with default values.
   Player () {
      this.hand = 0;
      this.reserves = 10000;
      this.isIn = false;
      this.pocket = new ArrayList<Integer>();
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
   public void setPocket (int card) {
      this.pocket.add(card);
   }
      
}