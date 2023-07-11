#version 330

#if defined VERTEX_SHADER

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;

out vec2 TexCoord;
out vec3 FragPos;
out vec3 Normal;

uniform mat4 model;
uniform mat4 camera;
uniform mat4 projection;
uniform float rotationAngle;
uniform vec3 scale;

void main() {
    mat4 view = camera * model;
    vec4 p = view * vec4(in_position * scale, 1.0);
    gl_Position =  projection * p;
    mat3 m_normal = inverse(transpose(mat3(view)));

    FragPos = p.xyz;
    Normal = m_normal * normalize(in_normal);
    TexCoord = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

out vec4 FragColor;

in vec2 TexCoord;
in vec3 FragPos;
in vec3 Normal;

uniform sampler2D texture1;
uniform vec3 lightPos;
uniform vec3 viewPos;

void main() {
    vec3 color = texture(texture1, TexCoord).rgb;

    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);

    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);

    vec3 ambient = 0.1 * color;
    vec3 diffuse = 0.8 * diff * color;
    vec3 specular = 0.2 * spec * vec3(1.0, 1.0, 1.0);

    FragColor = vec4(ambient + diffuse + specular, 1.0);
}

#endif
