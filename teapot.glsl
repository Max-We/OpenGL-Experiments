#version 330

#if defined VERTEX_SHADER

uniform mat4 m_model;
uniform mat4 m_camera;
uniform mat4 m_proj;
uniform vec3 Scale;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec3 v_vert;
out vec3 v_norm;
out vec2 v_text;

void main() {
    mat4 m_view = m_camera * m_model;
    vec4 p = m_view * vec4(in_position * Scale, 1.0);
    gl_Position = m_proj * p;

    v_vert = in_position * Scale;
    v_norm = in_normal;
    v_text = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER


uniform sampler2D Texture;
uniform vec4 Color;
uniform vec3 Light;
uniform vec3 CameraPosition; // Add a uniform for the camera position

in vec3 v_vert;
in vec3 v_norm;
in vec2 v_text;

out vec4 f_color;

void main() {
    float lum = dot(normalize(v_norm), normalize(v_vert - Light));
    lum = acos(lum) / 3.14159265;
    lum = clamp(lum, 0.0, 1.0);
    lum = lum * lum;
    lum = smoothstep(0.0, 1.0, lum);
    lum *= smoothstep(0.0, 80.0, v_vert.z) * 0.3 + 0.7;
    lum = lum * 0.8 + 0.2;

    vec3 color = texture(Texture, v_text).rgb;
    color = color * (1.0 - Color.a) + Color.rgb * Color.a;

    // Phong shading model
    vec3 ambient = 0.2 * color;
    vec3 diffuse = lum * color;

    // Specular component
    vec3 viewDirection = normalize(CameraPosition - v_vert);
    vec3 reflectDirection = reflect(normalize(v_vert - Light), normalize(v_norm));
    float spec = max(dot(viewDirection, reflectDirection), 0.0);
    float shininess = 32.0; // Adjust this value to control the glossiness
    vec3 specular = pow(spec, shininess) * vec3(1.0, 1.0, 1.0);

    f_color = vec4(ambient + diffuse + specular, 1.0);
}

//uniform sampler2D Texture;
//uniform vec4 Color;
//uniform vec3 Light;
//
//in vec3 v_vert;
//in vec3 v_norm;
//in vec2 v_text;
//
//out vec4 f_color;
//
//void main() {
//    float lum = dot(normalize(v_norm), normalize(v_vert - Light));
//    lum = acos(lum) / 3.14159265;
//    lum = clamp(lum, 0.0, 1.0);
//    lum = lum * lum;
//    lum = smoothstep(0.0, 1.0, lum);
//    lum *= smoothstep(0.0, 80.0, v_vert.z) * 0.3 + 0.7;
//    lum = lum * 0.8 + 0.2;
//
//    vec3 color = texture(Texture, v_text).rgb;
//    color = color * (1.0 - Color.a) + Color.rgb * Color.a;
//    f_color = vec4(color * lum, 1.0);
//}

#endif
