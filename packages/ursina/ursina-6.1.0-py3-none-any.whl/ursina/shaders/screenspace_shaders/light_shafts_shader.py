from ursina import Shader


light_shafts_shader = Shader(fragment='''
#version 430

uniform sampler2D tex;
in vec2 uv;
out vec4 COLOR;

in float density;
in float weight;
in float decay;
in float exposure;
flat in int numSamples;
// uniform sampler2D occlusionTexture;
in vec2 light_source_screen_position;

void main() {
		vec2 deltaTextCoord = vec2( uv - light_source_screen_position.xy );
    vec2 textCoo = uv.xy ;
    deltaTextCoord *= (1.0 /  float(numSamples)) * density;
    float illuminationDecay = 1.0;
		vec3 extra_light = vec3(0.0);

    for(int i=0; i < 100; i++){
	    	if(numSamples < i) {
            break;
	    	}

				textCoo -= deltaTextCoord;
				// vec3 samp = texture2D(occlusionTexture, textCoo   ).xyz;
				vec3 samp = texture2D(tex, textCoo).xyz;
				samp *= illuminationDecay * weight;
				extra_light += samp;
				illuminationDecay *= decay;
		}

  COLOR = vec4(texture(tex, uv).rgb + extra_light, 1.0);
	COLOR = vec4(extra_light, 1.0);
	// fragColor *= exposure;

    // vec3 rgb = texture(tex, uv).rgb;
    // float gray = rgb.r*.3 + rgb.g*.59 + rgb.b*.11;
}

''',
default_input = dict(
		density = 1.0,
		weight = 0.01,
		decay = 1.0,
		exposure = 1.0,
		numSamples = 100,
		light_source_screen_position = (0,0,0),
		)
)



if __name__ == '__main__':
    from ursina import *
    app = Ursina()
    window.color = color.white

    sun = Entity(model='sphere', scale=.05, position=(0,10,10))
    Entity(model='plane', scale=32, texture='grass')
    Entity(model='cube', scale_y=3, texture='brick', origin_y=-.5)
    Entity(model='cube', scale_y=3, texture='brick', origin_y=-.5, y=6, x=4)

    camera.shader = light_shafts_shader

    def update():
        camera.set_shader_input('light_source_screen_position', sun.screen_position)

    EditorCamera()

    app.run()
