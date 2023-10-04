from ursina import *; ssao_shader = Shader(language=Shader.GLSL, fragment='''
#version 140


uniform sampler2D tex;
uniform sampler2D dtex;
uniform mat4 p3d_ViewProjectionMatrix;

in vec2 uv;
out vec4 o_color;


void main() {
    o_color = texture(tex, uv);
    if (o_color.rgb == vec3(1.,0.,1.)) {      // if magenta
        o_color = texture(tex, uv+vec2(0.0, 0.2));
        o_color /= 2.;
        // o_color = vec4(0,0,1,1);
    }
}
''',

default_input = {
}
)

if __name__ == '__main__':
    from ursina import *
    app = Ursina(vsync=False)

    # from ursina.shaders import lit_with_shadows_shader
    # Entity.default_shader = lit_with_shadows_shader
    Sky(scale=450)
    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    e = Entity(model='plane', scale=100, y=-1, texture='grass')
    e = Entity(model='plane', scale=3, y=0, color=color.magenta)
    camera.shader = ssao_shader
    camera.clip_plane_far = 500
    # camera.clip_plane_near = 1

    EditorCamera()

    app.run()
