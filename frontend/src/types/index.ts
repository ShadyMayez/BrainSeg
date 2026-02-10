export interface PredictionResponse {
  status: string;
  segmentation_mask: string;
  overlay_image: string | null;
  tumor_stats: Record<string, {
    pixel_count: number;
    percentage: number;
  }>;
  class_distribution: Record<string, {
    pixel_count: number;
    percentage: number;
  }>;
  slice_thickness: number | null;
  processed_slices: number;
  input_shape: number[];
  model_used: string;
}

export interface HealthStatus {
  status: string;
  service: string;
  version: string;
  framework: string;
}

export interface FileUploadState {
  flair: File | null;
  t1ce: File | null;
}

export interface ModalityInfo {
  name: string;
  description: string;
  required: boolean;
}

// Only 2 modalities required (matching Kaggle notebook)
export const MODALITIES: ModalityInfo[] = [
  {
    name: 'flair',
    description: 'T2-FLAIR - Fluid Attenuated Inversion Recovery',
    required: true
  },
  {
    name: 't1ce',
    description: 'T1CE - T1 with Gadolinium contrast enhancement',
    required: true
  }
];

export const CLASS_LABELS: Record<number, string> = {
  0: 'Non-tumor',
  1: 'Necrotic/Core',
  2: 'Edema',
  3: 'Enhancing Tumor'
};

export const CLASS_COLORS: Record<number, string> = {
  0: '#000000',
  1: '#0000FF',
  2: '#FFC0CB',
  3: '#00FFFF'
};
