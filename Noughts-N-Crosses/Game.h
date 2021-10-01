// Game.h
// Primarily just the game class that Game.cpp elaborates on

// Primary Arduboy Libraries
#include <Arduboy2.h> 
#include <ArduboyTones.h>
#include "classes.h"

class Game {
  public:
    // Game Functions
    void gameBoot();
    void gameLoop();

    void titleLogic();
    void titleDraw();

    void gameLogic();
    void gameDraw();

    bool drawCheck();
    Cell winCheck();

    // Set up arduboy object + Sound
    Arduboy2 arduboy;
    ArduboyTones arSound = ArduboyTones(arduboy.audio.enabled);


    Cell player = Cell::Cross; // No P1/P2, the main "Player" variable is switched between Cross and Nought
    Cell winner;
    Cell grid[3][3];

    States gameState = States::Main; // Game defaults to "Main" state [No Winnter, Not Paused]
    States gameScreen;

    Point2 selector;
    Point2 winningSets[8][3] = { // All combinations of winning scenarios
      {{0, 0}, {0, 1}, {0, 2}},
      {{1, 0}, {1, 1}, {1, 2}},
      {{2, 0}, {2, 1}, {2, 2}},

      {{0, 0}, {1, 0}, {2, 0}},
      {{0, 1}, {1, 1}, {2, 1}},
      {{0, 2}, {1, 2}, {2, 2}},

      {{0, 0}, {1, 1}, {2, 2}},
      {{0, 2}, {1, 1}, {2, 0}}
   };
  
  private: // Images [Loaded with bitmap values in game.cpp]
    static const unsigned char splash[];

    static const unsigned char title[];

    static const unsigned char board[];
    
    static const unsigned char cross[];
    static const unsigned char nought[];
    static const unsigned char selector_[];
};

// OxygenCobalt