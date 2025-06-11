

spa_wait_azimuth: spa_wait_azimuth.c spa.c Makefile
	gcc -g -I. -o spa_wait_azimuth spa_wait_azimuth.c spa.c -lm


install:  spa_wait_azimuth
	mv spa_wait_azimuth ~reilly/`arch`/spa
