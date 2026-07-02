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

export class AetherRenderer {
  private canvas: HTMLCanvasElement;
  // TODO: webgl/webgpu context, shaders, buffers

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    // init WebGL/WebGPU context here
  }

  public update(ir: IR8D) {
    // TODO: map IR8D → uniforms, SDF fields, particle flow
    console.log("Renderer updated with IR:", ir);
  }

  public resize(width: number, height: number) {
    this.canvas.width = width;
    this.canvas.height = height;
    // adjust viewport
  }
}
