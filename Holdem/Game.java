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
      
      game.printHands();
      
      game.flop();
      game.turn();
      game.river();
            
      /* DEBUGGING
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
      */
   }
}
