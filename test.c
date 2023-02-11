#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>
#include <GLES3/gl3.h>
#include <stdbool.h>
#include <emscripten.h>

#define PNG_FILE "assets/sample.png"
#define JPG_FILE "assets/sample.jpg"
#define MP3_FILE "assets/sample.mp3"
#define OGG_FILE "assets/sample.ogg"
Mix_Music *music_mp3=NULL;
Mix_Music *music_ogg=NULL;
Mix_Music *playing_music = NULL;

static void mixer_init()
{
  printf("open_audio\n");
  Mix_Init(MIX_INIT_MP3|MIX_INIT_OGG);
  if( Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, MIX_DEFAULT_CHANNELS, 4096) == 0 ){
    printf("Mix_OpenAudio succeeded.\n");
  }else{
    printf("Mix_OpenAudio failed.\n");
  }
  int channels = Mix_AllocateChannels(16);
  printf("%d channels allocated\n", channels);
  Mix_VolumeMusic(MIX_MAX_VOLUME/4);

  music_mp3 = Mix_LoadMUS_RW(SDL_RWFromFile(MP3_FILE,"rb"),SDL_TRUE);
  if(music_mp3==NULL) printf("mp3 load failed.\n");
  music_ogg = Mix_LoadMUS_RW(SDL_RWFromFile(OGG_FILE,"rb"),SDL_TRUE);
  if(music_ogg==NULL) printf("ogg load failed\n");
}

static void set_music_position(double pos)
{
  if(playing_music){
    pos = Mix_MusicDuration(playing_music) * pos;
    printf("Set Position %.2f sec\n",pos);
    Mix_SetMusicPosition( pos );
  }
}

static void play_music(Mix_Music *music)
{
  playing_music = music;
  // Mix_PlayMusic(music, 0);
  Mix_FadeInMusic(music,-1,3000);
}


static void main_loop( void* arg )
{
  SDL_Event e;
  while (SDL_PollEvent(&e)) {
    switch (e.type) {
    case SDL_MOUSEMOTION:
      Mix_VolumeMusic(MIX_MAX_VOLUME * e.motion.y / 240.0 );
      break;
    case SDL_MOUSEBUTTONDOWN:
      if(e.button.button==SDL_BUTTON_RIGHT) {
        // stutter
        for(int i=0;i<3;i++){
          printf("Stutter %dsec...\n",3-i);
          SDL_Delay(1000);
        }
      }else{
        if( Mix_PlayingMusic() ){
          set_music_position( e.button.x / 320.0 );
        }
      }
      break;
    case SDL_KEYDOWN:
      if(e.key.keysym.sym == SDLK_m){
        printf("play mp3\n");
        play_music(music_mp3);
      }else if(e.key.keysym.sym == SDLK_o){
        printf("play ogg\n");
        play_music(music_ogg);
      }
      break;
    case SDL_QUIT:
      exit(0);
      break;
    }
  }
}

int main(int argc, char *argv[])
{
  SDL_Init(SDL_INIT_VIDEO);

  SDL_version compiled;
  SDL_version linked;
  SDL_VERSION(&compiled);
  SDL_GetVersion(&linked);
  printf("SDL(compile): %u.%u.%u\n",
         compiled.major, compiled.minor, compiled.patch);
  printf("SDL(link) : %u.%u.%u\n",
         linked.major, linked.minor, linked.patch);

  SDL_SetHint(SDL_HINT_RENDER_DRIVER,"opengl");
  SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_ES);
  SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3);
  SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 0);

  Uint32 flag = SDL_WINDOW_OPENGL;
  SDL_Window* window = SDL_CreateWindow(__FILE__, SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 320, 240, flag);
  SDL_Renderer *render = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

  SDL_GLContext *glcontext = SDL_GL_CreateContext(window);
  if(glcontext==NULL){
    printf("SDL_GL_CreateContext failed: %s\n",SDL_GetError());
    exit(1);
  }
  printf("GL_VENDOR: %s\n", glGetString(GL_VENDOR));
  printf("GL_VERSION: %s\n", glGetString(GL_VERSION));
  printf("GL_RENDERER: %s\n", glGetString(GL_RENDERER));
  printf("GL_SHADING_LANGUAGE_VERSION: %s\n", glGetString(GL_SHADING_LANGUAGE_VERSION));

  if( IMG_Init(IMG_INIT_PNG) == 0 ){
    printf("image init failed.\n");
  }
  SDL_Surface* img_png = IMG_Load(PNG_FILE);
  SDL_Surface* img_jpg = IMG_Load(JPG_FILE);
  if(img_png==NULL) { printf("png load failed\n"); }
  if(img_jpg==NULL) { printf("jpg load failed\n"); }
  SDL_RenderClear(render);
  SDL_Rect png_dst = {0,0,160,240};
  SDL_Rect jpg_dst = {160,0,160,240};
  SDL_RenderCopy(render, SDL_CreateTextureFromSurface(render,img_png), NULL, &png_dst);
  SDL_RenderCopy(render, SDL_CreateTextureFromSurface(render,img_jpg), NULL, &jpg_dst);
  SDL_RenderPresent(render);

  mixer_init();

  emscripten_set_main_loop_arg(main_loop, NULL, 0, false);
}
