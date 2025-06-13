#include <time.h> 
#include <assert.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>

// nyc sun hits the east window
//  Azimuth:       209.366093 degrees

// in nyc this may be when sun stops hitting east window
// Azimuth:       298.965935 degrees   or ~299
//   in correct elevation it appears to be 270

/////////////////////////////////////////////
//          SPA TESTER for SPA.C           //
//                                         //
//      Solar Position Algorithm (SPA)     //
//                   for                   //
//        Solar Radiation Application      //
//                                         //
//             August 12, 2004             //
//                                         //
//   Filename: SPA_TESTER.C                //
//                                         //
//   Afshin Michael Andreas                //
//   afshin_andreas@nrel.gov (303)384-6383 //
//                                         //
//   Measurement & Instrumentation Team    //
//   Solar Radiation Research Laboratory   //
//   National Renewable Energy Laboratory  //
//   1617 Cole Blvd, Golden, CO 80401      //
/////////////////////////////////////////////

/////////////////////////////////////////////
// This sample program shows how to use    //
//    the SPA.C code.                      //
/////////////////////////////////////////////

#include <stdio.h>
#include "spa.h"  //include the SPA header file

int verbose=0;

int main (int argc, char *argv[])
{
    spa_data spa;  //declare the SPA structure
    int result;
    float min, sec;

    struct tm mytm;
    time_t now;

    double azwait;


// see if any options were specified, and act like before if nothing

    struct option longopts;
    int option_index;
    int c;


               static struct option long_options[] = {
                   {"wait",     required_argument, 0,  0 },
		   //                   {"append",  no_argument,       0,  0 },
		   //                   {"delete",  required_argument, 0,  0 },
		   {"verbose", no_argument,       0,  0 },
		   //                   {"create",  required_argument, 0, 'c'},
		   //                   {"file",    required_argument, 0,  0 },
                   {0,         0,                 0,  0 }
               };




	       while ( -1 != ( c = getopt_long_only(argc
						    ,argv
						    ,""
						    ,long_options	
						    ,&option_index)))
      {


               switch (c) {
               case 0:
		 if (verbose) 
		   printf("0 option %s", long_options[option_index].name);
                   if (optarg && verbose)
                       printf(" with arg %s", optarg);
		   if (verbose) printf("\n");

		   if (0==strcmp(long_options[option_index].name,"wait"))
		     azwait = atof(optarg);

		   if (0==strcmp(long_options[option_index].name,"verbose"))
		     verbose = 1;


                   break;

	       default:

                   printf("def option %s", long_options[option_index].name);

                   if (optarg)
                       printf(" with arg %s", optarg);
                   printf("\n");



                   break;
	       } /* switch */





}



    time(&now);


    while(1) 
        {                                        /* wait to pass az */



    localtime_r(&now,&mytm);


#ifdef GBR
    assert(argc==2);
    azwait = atof(argv[1]);

#endif

    assert(azwait>0.0);


    //enter required input values into SPA structure

    spa.year          = mytm.tm_year+1900;
    spa.month         = mytm.tm_mon+1;
    spa.day           = mytm.tm_mday;
    spa.hour          = mytm.tm_hour;
    spa.minute        = mytm.tm_min;
    spa.second        = mytm.tm_sec;
    spa.timezone      = -5.0 + mytm.tm_isdst;                      /* was -5.0 */
    spa.delta_t       = 67;
    //http://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q=138+milbank,06830&sll=41.027312,-73.64994&sspn=0.275578,0.297661&ie=UTF8&hq=&hnear=138+Milbank+Ave,+Greenwich,+Fairfield,+Connecticut+06830&ll=41.030971,-73.622131&spn=0.034445,0.037208&z=15

    spa.longitude     = /* -75.153405 */  /*-73.622131 */  -73.976434;
    spa.latitude      = /* 39.945387 */  /*41.030971 */ 40.749848;
    spa.elevation     =  18  + 16 /* 1830.14*/ ;  /* !!!THIS MUST BE WRONG*/
    spa.pressure      = 820;
    spa.temperature   = 11;
    spa.slope         = 30;
    spa.azm_rotation  = -10;
    spa.atmos_refract = 0.5667;
    spa.function      = SPA_ALL;

    //call the SPA calculate function and pass the SPA structure

    result = spa_calculate(&spa);

    assert(result==0);

      if (spa.azimuth+13.0+(44/60)> azwait)
	{ 
	  if ( verbose ) {
	    printf ("exiting since %.2f > %.2f\n"
		    ,spa.azimuth+13.0+(44/60)
		    ,azwait
		    );
	  } /* verbose */


	  exit(0); 
	}   /* if spa .. >  */

	
        now = now + 300;
	sleep(300); 

	//	printf("DEBUG %f at %d\n",spa.azimuth+13.0+(44/60),__LINE__);

        assert(mytm.tm_hour<22);


       } /* while */

      printf("Time:  %s\n\n", ctime(&now));


    if (result == 0)  //check for SPA errors
    {
        //display the results inside the SPA structure

        printf("Julian Day:    %.6f\n",spa.jd);
        printf("L:             %.6e degrees\n",spa.l);
        printf("B:             %.6e degrees\n",spa.b);
        printf("R:             %.6f AU\n",spa.r);
        printf("H:             %.6f degrees\n",spa.h);
        printf("Delta Psi:     %.6e degrees\n",spa.del_psi);
        printf("Delta Epsilon: %.6e degrees\n",spa.del_epsilon);
        printf("Epsilon:       %.6f degrees\n",spa.epsilon);
        printf("Zenith:        %.6f degrees\n",spa.zenith);
        printf("Azimuth:       %.6f degrees (corrected for 13 44' declination)\n",spa.azimuth+13.0+(44/60));
        printf("Incidence:     %.6f degrees\n",spa.incidence);

        min = 60.0*(spa.sunrise - (int)(spa.sunrise));
        sec = 60.0*(min - (int)min);
        printf("Sunrise:       %02d:%02d:%02d Local Time\n", (int)(spa.sunrise), (int)min, (int)sec);  /*  THIS IS WRONG -- ONE HOUR LOW IN EDT */

        min = 60.0*(spa.sunset - (int)(spa.sunset));
        sec = 60.0*(min - (int)min);
        printf("Sunset:        %02d:%02d:%02d Local Time\n", (int)(spa.sunset), (int)min, (int)sec);

    } else printf("SPA Error Code: %d\n", result);

    return 0;
}

/////////////////////////////////////////////
// The output of this program should be:
//
//Julian Day:    2452930.312847
//L:             2.401826e+01 degrees
//B:             -1.011219e-04 degrees
//R:             0.996542 AU
//H:             11.105902 degrees
//Delta Psi:     -3.998404e-03 degrees
//Delta Epsilon: 1.666568e-03 degrees
//Epsilon:       23.440465 degrees
//Zenith:        50.111622 degrees
//Azimuth:       194.340241 degrees
//Incidence:     25.187000 degrees
//Sunrise:       06:12:43 Local Time
//Sunset:        17:20:19 Local Time
//
/////////////////////////////////////////////

