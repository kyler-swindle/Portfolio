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

// The Game Class is where both of the other two classes are implemented
// to create the Texas Hold'em Game.  
class Game {

   public static void main (String[] args) {
      Table game = new Table(5);
      
      for (int i = 0; i < game.players.size(); i++) {
         for (int j = 0; j < 2; j++) {
            if (j == 0) {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.print(game.decodeCard(game.players.get(i).getPocket().get(j)) + ", ");
            } else {
               System.out.print(game.players.get(i).getPocket().get(j) + ":");
               System.out.println(game.decodeCard(game.players.get(i).getPocket().get(j)) + ".");
            }
         }
      }
   }
   
}