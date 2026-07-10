export interface IR8D {
  x: number;
  y: number;
  z: number;
  semantic_intent: string;
  confidence: number;
  energy_level: number;
  ontological_persistence: number;
  policy_risk: number;
  color?: string;
}

export interface ManifestContract {
  intent: string;
  archetype: string;
  topology: string;
  parameters: Record<string, any>;
  ir: IR8D;
}

export interface RenderProfile {
  color: string;
  particleDensity: number;
  flowSpeed: number;
  baseGeometry: string;
}

export class RenderProfileResolver {
  public resolve(contract: ManifestContract): RenderProfile {
    let baseColor = "#FFFFFF";

    if (contract.ir.energy_level > 0.8) {
       baseColor = "#FF3366";
    } else if (contract.intent === "TREE") {
       baseColor = "#33FF99";
    } else if (contract.intent === "VORTEX") {
       baseColor = "#3366FF";
    }

    if (contract.intent === "UNKNOWN" && contract.ir.semantic_intent === "VOID") {
        baseColor = contract.ir.color || "#0B1026";
    }

    return {
      color: baseColor,
      particleDensity: contract.parameters.density || 1.0,
      flowSpeed: contract.parameters.rotation_speed || 1.0,
      baseGeometry: contract.topology
    };
  }
}

const VERTEX_SHADER_SRC = `
  attribute vec2 a_position;
  varying vec2 v_uv;
  void main() {
    v_uv = a_position * 0.5 + 0.5;
    gl_Position = vec4(a_position, 0.0, 1.0);
  }
`;

const FRAGMENT_SHADER_SRC = `
  precision mediump float;
  varying vec2 v_uv;
  uniform float u_time;
  uniform vec2 u_resolution;
  uniform vec3 u_color;
  uniform float u_particleDensity;
  uniform float u_flowSpeed;

  void main() {
    vec2 st = gl_FragCoord.xy / u_resolution.xy;
    st.x *= u_resolution.x / u_resolution.y;

    vec2 center = vec2(0.5 * (u_resolution.x / u_resolution.y), 0.5);
    float d = distance(st, center);

    // Basic SDF circle + time-based ripple
    float ripple = sin(d * 20.0 * u_particleDensity - u_time * u_flowSpeed) * 0.5 + 0.5;
    float circle = smoothstep(0.4, 0.38, d);

    vec3 col = u_color * ripple * circle;

    // Background
    vec3 bg = vec3(0.043, 0.063, 0.149); // #0B1026

    gl_FragColor = vec4(mix(bg, col, circle), 1.0);
  }
`;

function hexToRgb(hex: string): [number, number, number] {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? [
    parseInt(result[1], 16) / 255,
    parseInt(result[2], 16) / 255,
    parseInt(result[3], 16) / 255
  ] : [1, 1, 1];
}

export class AetherRenderer {
  private canvas: HTMLCanvasElement;
  private gl: WebGLRenderingContext | null;
  private program: WebGLProgram | null = null;
  private animationFrameId: number = 0;
  private startTime: number;
  private positionBuffer: WebGLBuffer | null = null;
  private vertexShader: WebGLShader | null = null;
  private fragmentShader: WebGLShader | null = null;

  private currentProfile: RenderProfile | null = null;

  // Uniform locations
  private uTimeLoc: WebGLUniformLocation | null = null;
  private uResolutionLoc: WebGLUniformLocation | null = null;
  private uColorLoc: WebGLUniformLocation | null = null;
  private uParticleDensityLoc: WebGLUniformLocation | null = null;
  private uFlowSpeedLoc: WebGLUniformLocation | null = null;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    this.gl = this.canvas.getContext('webgl');
    this.startTime = performance.now();

    if (this.gl) {
      this.initWebGL();
    } else {
      console.error("WebGL not supported");
    }
  }

  private compileShader(gl: WebGLRenderingContext, type: number, source: string): WebGLShader | null {
    const shader = gl.createShader(type);
    if (!shader) return null;

    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.error('Shader compilation error:', gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }

    return shader;
  }

  private initWebGL() {
    const gl = this.gl;
    if (!gl) return;

    this.vertexShader = this.compileShader(gl, gl.VERTEX_SHADER, VERTEX_SHADER_SRC);
    this.fragmentShader = this.compileShader(gl, gl.FRAGMENT_SHADER, FRAGMENT_SHADER_SRC);

    if (!this.vertexShader || !this.fragmentShader) return;

    this.program = gl.createProgram();
    if (!this.program) return;

    gl.attachShader(this.program, this.vertexShader);
    gl.attachShader(this.program, this.fragmentShader);
    gl.linkProgram(this.program);

    if (!gl.getProgramParameter(this.program, gl.LINK_STATUS)) {
      console.error('Program linking error:', gl.getProgramInfoLog(this.program));
      return;
    }

    // Set up full-screen quad
    const positions = new Float32Array([
      -1.0, -1.0,
       1.0, -1.0,
      -1.0,  1.0,
      -1.0,  1.0,
       1.0, -1.0,
       1.0,  1.0,
    ]);

    this.positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);

    const positionLocation = gl.getAttribLocation(this.program, "a_position");
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

    // Get uniform locations
    this.uTimeLoc = gl.getUniformLocation(this.program, "u_time");
    this.uResolutionLoc = gl.getUniformLocation(this.program, "u_resolution");
    this.uColorLoc = gl.getUniformLocation(this.program, "u_color");
    this.uParticleDensityLoc = gl.getUniformLocation(this.program, "u_particleDensity");
    this.uFlowSpeedLoc = gl.getUniformLocation(this.program, "u_flowSpeed");

    this.renderLoop();
  }

  public update(profile: RenderProfile, contract: ManifestContract) {
    this.currentProfile = profile;
    console.log("Renderer updated with Profile:", profile, "Contract:", contract);
  }

  public resize(width: number, height: number) {
    this.canvas.width = width;
    this.canvas.height = height;
    if (this.gl) {
      this.gl.viewport(0, 0, width, height);
    }
  }

  private renderLoop = () => {
    const gl = this.gl;
    if (!gl || !this.program) return;

    gl.useProgram(this.program);

    const time = (performance.now() - this.startTime) / 1000.0;
    gl.uniform1f(this.uTimeLoc, time);
    gl.uniform2f(this.uResolutionLoc, gl.canvas.width, gl.canvas.height);

    if (this.currentProfile) {
      const color = hexToRgb(this.currentProfile.color);
      gl.uniform3f(this.uColorLoc, color[0], color[1], color[2]);
      gl.uniform1f(this.uParticleDensityLoc, this.currentProfile.particleDensity);
      gl.uniform1f(this.uFlowSpeedLoc, this.currentProfile.flowSpeed);
    } else {
      gl.uniform3f(this.uColorLoc, 1.0, 1.0, 1.0);
      gl.uniform1f(this.uParticleDensityLoc, 1.0);
      gl.uniform1f(this.uFlowSpeedLoc, 1.0);
    }

    gl.drawArrays(gl.TRIANGLES, 0, 6);

    this.animationFrameId = requestAnimationFrame(this.renderLoop);
  }

  public dispose() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    if (this.gl) {
      if (this.program) {
        this.gl.deleteProgram(this.program);
      }
      if (this.vertexShader) {
        this.gl.deleteShader(this.vertexShader);
      }
      if (this.fragmentShader) {
        this.gl.deleteShader(this.fragmentShader);
      }
      if (this.positionBuffer) {
        this.gl.deleteBuffer(this.positionBuffer);
      }
    }
  }
}
