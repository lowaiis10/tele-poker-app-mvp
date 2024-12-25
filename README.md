# solana-project
![image](https://github.com/user-attachments/assets/3d961602-a643-43d2-887f-e2c91314ec0a)

SRC
- main.py ( entry point to start bot )
- bot
  -- front_end.py ( where the button uis are held )
  -- middleware.py ( where updates from user actions are processed )
  -- handlers.py ( logic for buttons based on updates from middle ware )
- poker_mechanics
  -- [ x ] database.py ( storing games and updating game states asynchronously )
  -- [ x ] game_logic ( Actual poker mechanics and gameplay logic )
  -- [ x ] game_mechanics ( Broadcast and maintain perfect information of game state to all private chats )
- solana
 -- [ x ] wallet.py ( deeplinks for phantom intgration )

* [ x ] = To do
  
