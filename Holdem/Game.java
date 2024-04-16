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

// The Game Class is where both of the other two classes are implemented
// to create the Texas Hold'em Game.  

import java.util.ArrayList; // - used for debugging to pass ArrayLists through
                              // method calls via the declared Table instance, game. 
                                 
import java.util.Arrays; // ---- also used for debugging to pass ArrayLists through
                              // method calls via the declared Table instance, game.
                              
import java.lang.Math; // ------ debugging

class Game {

   public static void main (String[] args) {
      Table game = new Table(5);
            
      System.out.println("\nPlayers: ");
      for (int i = 0; i < game.players.size(); i++) {
         for (int j = 0; j < 2; j++) {
            if (j == 0) {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ", ");
            } else {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ".");
            }
         }
         
         System.out.println(" Hand: " + game.decodeHand(game.players.get(i).getHand()));
      }
      
      System.out.println("\nFlop: ");
      game.flop();
      for (int i = 0; i < game.table.size(); i++) {
            if (i == game.table.size() - 1) {
               System.out.print(game.table.get(i) + ":");
               System.out.println(game.decodeCard(game.table.get(i)) + ". ");
            } else {
               System.out.print(game.table.get(i) + ":");
               System.out.print(game.decodeCard(game.table.get(i)) + ", ");
            }
      }
            
      System.out.println("\nPlayers: ");
      for (int i = 0; i < game.players.size(); i++) {
         for (int j = 0; j < 2; j++) {
            if (j == 0) {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ", ");
            } else {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ".");
            }
         }
         
         System.out.println(" Hand: " + game.decodeHand(game.players.get(i).getHand()));
      }
      
      System.out.println("\nTurn: ");
      game.turn();
      for (int i = 0; i < game.table.size(); i++) {
            if (i == game.table.size() - 1) {
               System.out.print(game.table.get(i) + ":");
               System.out.println(game.decodeCard(game.table.get(i)) + ". ");
            } else {
               System.out.print(game.table.get(i) + ":");
               System.out.print(game.decodeCard(game.table.get(i)) + ", ");
            }
      }
      
      System.out.println("\nPlayers: ");
      for (int i = 0; i < game.players.size(); i++) {
         for (int j = 0; j < 2; j++) {
            if (j == 0) {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ", ");
            } else {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ".");
            }
         }
         
         System.out.println(" Hand: " + game.decodeHand(game.players.get(i).getHand()));
      }
      
      System.out.println("\nRiver: ");
      game.river();
      for (int i = 0; i < game.table.size(); i++) {
            if (i == game.table.size() - 1) {
               System.out.print(game.table.get(i) + ":");
               System.out.println(game.decodeCard(game.table.get(i)) + ". ");
            } else {
               System.out.print(game.table.get(i) + ":");
               System.out.print(game.decodeCard(game.table.get(i)) + ", ");
            }
      }
      
      System.out.println("\nPlayers: ");
      for (int i = 0; i < game.players.size(); i++) {
         for (int j = 0; j < 2; j++) {
            if (j == 0) {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ", ");
            } else {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ".");
            }
         }
         
         System.out.println(" Hand: " + game.decodeHand(game.players.get(i).getHand()));
      }
      
      System.out.println("\nHighest Hand: Player:" + game.currHighestHand() + " - " + game.decodeHand(game.players.get(game.currHighestHand()).getHand()) + " (" + game.players.get(game.currHighestHand()).getHand() + ")");
      
      /*
      game.removePlayers(new ArrayList(Arrays.asList(0,1,2,3)));
      
      
      game.table.set(0, 17);
      game.table.set(1, 27);
      game.table.set(2, 50);
      game.table.set(3, 51);
      game.table.set(4, 39);
      
      game.resetPlayers();
      
      game.players.get(0).setPocket(new ArrayList(Arrays.asList(18, 16)));
      game.players.get(1).setPocket(new ArrayList(Arrays.asList(33, 23)));
      game.players.get(2).setPocket(new ArrayList(Arrays.asList(29, 8)));
      game.players.get(3).setPocket(new ArrayList(Arrays.asList(21, 26)));
      game.players.get(4).setPocket(new ArrayList(Arrays.asList(19, 48)));
      game.postCard();
      
      for (int i = 0; i < game.table.size(); i++) {
            if (i == game.table.size() - 1) {
               System.out.print(game.table.get(i) + ":");
               System.out.println(game.decodeCard(game.table.get(i)) + ". ");
            } else {
               System.out.print(game.table.get(i) + ":");
               System.out.print(game.decodeCard(game.table.get(i)) + ", ");
            }
      }
      
      System.out.println("\nPlayers: ");
      for (int i = 0; i < game.players.size(); i++) {
         for (int j = 0; j < 2; j++) {
            if (j == 0) {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ", ");
            } else {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ".");
            }
         }
         
         System.out.println(" Hand: " + game.decodeHand(game.players.get(i).getHand()));
      }
      
      System.out.println("\nHighest Hand: Player:" + game.currHighestHand() + " - " + game.decodeHand(game.players.get(game.currHighestHand()).getHand()));
      
      
      for (int i = 0; i < 52; i++) {
         // System.out.println(i + ":" + i % 4 + ":" + i / 4 + ":" + i / 13 + ":" + i % 13);
         System.out.println(i + ":" + i / 4+ ":" + game.decodeCard(i));
      }
      */
   }
}
