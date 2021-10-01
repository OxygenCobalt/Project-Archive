// Classes.h
// Primary storage for classes, such as game states and an X-Y coordinate format

#pragma once

enum class States : uint8_t {
  // All screens/states of game

  Title, Game,
  
  Main, Paused, Winner
};

enum class Cell : uint8_t {
  // Cell format for tic-tac-toe
  // Also used for player types
  // Empty [Editable], Cross/Nought [Non-Editable]
  Empty, Cross, Nought
};

class Point2 {
  // X-Y system developed by pharap
  // Used to keep track of selectors and cell positions
  public:
   int16_t x;
   int16_t y;
  
   Point2(void) = default; // Not a function type
   Point2(int16_t x, int16_t y) : x(x), y(y) {} // Set x/y as specific values
};

// OxygenCobalt
