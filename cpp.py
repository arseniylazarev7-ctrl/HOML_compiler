MainCpp =\
"""
#define SDL_MAIN_USE_CALLBACKS 1
#include <SDL3/SDL_main.h>
#include "/*ClassName*/.h"

/*ClassName*/ /*Name*/;

SDL_AppResult SDL_AppInit(void** appstate, int argc, char* argv[]) {
	return /*Name*/.SDL_AppInit();
}
SDL_AppResult SDL_AppEvent(void* appstate, SDL_Event* event) {
	return /*Name*/.SDL_AppEvent(event);
}
SDL_AppResult SDL_AppIterate(void* appstate) {
	return /*Name*/.SDL_AppIterate();
}

void SDL_AppQuit(void* appstate, SDL_AppResult result) {
	/*Name*/.SDL_AppQuit(result);
}
"""

ClassAppAppH =\
"""
class /*ClassName*/ {
public:
	// These are tools for drawing on window
	SDL_Window* window;
	SDL_Renderer* renderer;

	// These are devices for tracking user actions
	Mouse mouse;
	Keyboard keyboard;

	// These are variables on your application
	/*vars*/

	// These are pages on your application
	/*pages*/

	// These are SDL functions, better not touch them 
	SDL_AppResult SDL_AppInit();
	SDL_AppResult SDL_AppEvent(SDL_Event* event);
	SDL_AppResult SDL_AppIterate();
	void SDL_AppQuit(SDL_AppResult result);

	// These are main methods your application
	SDL_AppResult init();
	SDL_AppResult loop();
	SDL_AppResult event(SDL_Event* event);
};
"""

ClassAppAppCpp =\
"""
#include "/*ClassName*/.h"

SDL_AppResult /*ClassName*/::init() {
	SDL_Init(SDL_INIT_VIDEO);
	TTF_Init();
	SDL_CreateWindowAndRenderer("/*Name*/", /*Width*/, /*Height*/, 0, &window, &renderer);

/*Init()*/

	return SDL_AppResult();
}

SDL_AppResult /*ClassName*/::loop() {

/*Loop()*/

	return SDL_APP_CONTINUE;
}

SDL_AppResult /*ClassName*/::event(SDL_Event* event) {
	
}

SDL_AppResult /*ClassName*/::SDL_AppInit() {
	return this->init();
}

SDL_AppResult /*ClassName*/::SDL_AppIterate() {
	return this->loop();
}

SDL_AppResult /*ClassName*/::SDL_AppEvent(SDL_Event* event) {
	return this->event(event)
}

void /*ClassName*/::SDL_AppQuit(SDL_AppResult result) {

}
"""

StartH =\
"""
#pragma once
#include <SDL3/SDL.h>
#include <SDL3_ttf/SDL_ttf.h>
#include <SDL3_image/SDL_image.h>
"""