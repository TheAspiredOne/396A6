// C++ code fragment for printing Webbels states (regular or coloured)
//
// This file will not compile because I just copied it from my solution
// So, please copy and paste whatever part you need for your program


// useful macro for common for-loops (0..n-1)
#define FOR(i, n) for (decltype((n)+(n)) i=0; i < (n); ++i)

/*
  color terminal strings
  
  text attributes: \x1b[{attr};{fg};{bg}m

  clear screen: "\x1b[2J"
  cursor home:  "\x1b[H"
  
Text attributes
       0    All attributes off
       1    Bold on
       4    Underscore (on monochrome display adapter only)
       5    Blink on
       7    Reverse video on
       8    Concealed on

      Foreground colours
       30    Black
       31    Red
       32    Green
       33    Yellow
       34    Blue
       35    Magenta
       36    Cyan
       37    White

      Background colours
       40    Black
       41    Red
       42    Green
       43    Yellow
       44    Blue
       45    Magenta
       46    Cyan
       47    White
*/

static const string CONT_STRINGS[] = { "--", "oo", "xx", "$$", "##", "++", "@@" };

static_assert(sizeof(CONT_STRINGS)/sizeof(CONT_STRINGS[0]) > State::MAX_COLOURS,
              "not enough entries");

static const string COLOUR_STRINGS[] = {
  "",
  "\x1b[1;37;41m",
  "\x1b[1;37;42m",
  "\x1b[1;37;43m",
  "\x1b[1;37;44m",
  "\x1b[1;37;45m",
  "\x1b[1;37;46m",
  "\x1b[1;37;47m"
};

static_assert(sizeof(COLOUR_STRINGS)/sizeof(COLOUR_STRINGS[0]) > State::MAX_COLOURS,
              "not enough entries");
              

void State::write(bool colour, int x0, int y0) const
{
  const string reset = "\x1b[0m";

  if (colour) {
    cout << "\x1b[2J"; // clear
    cout << "\x1b[H";  // home
  }
  
  for (int y=sy-1; y >= 0; --y) {
    cout << y << "|";
    FOR (x, sx) {
      // 2 characters per cell
      if (colour) {
        // coloured
        cout << COLOUR_STRINGS[cont(x, y)] << ((x == x0 && y == y0) ? "##" : "  ") << reset;
      } else {
        // regular
        cout << CONT_STRINGS[cont(x, y)];
      }      
    }
    cout << "|" << endl;
  }

  cout << "  ";
  FOR (x, sx) {
    cout << x << " ";
  }
  cout << endl;
  
  if (x0 >= 0) {
    cout << "move: " << x0 << " " << y0 << endl;
  }
}