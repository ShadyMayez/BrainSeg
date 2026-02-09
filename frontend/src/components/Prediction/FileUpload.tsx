import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface FileUploadProps {
  label: string;
  description: string;
  file: File | null;
  onFileSelect: (file: File | null) => void;
  accept?: string;
}

export function FileUpload({ 
  label, 
  description, 
  file, 
  onFileSelect,
  accept = '.nii,.nii.gz,.gz' 
}: FileUploadProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive, isDragAccept, isDragReject } = useDropzone({
    onDrop,
    // Accept common NIfTI and gzip extensions. Use generic binary MIME for .nii
    accept: {
      'application/octet-stream': ['.nii', '.nii.gz'],
      'application/gzip': ['.gz', '.nii.gz'],
      'application/x-gzip': ['.gz', '.nii.gz'],
    },
    multiple: false,
  });

  const clearFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    onFileSelect(null);
  };

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      
      {file ? (
        <div className="flex items-center gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
          <File className="w-8 h-8 text-green-600" />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">{file.name}</p>
            <p className="text-xs text-gray-500">
              {(file.size / (1024 * 1024)).toFixed(2)} MB
            </p>
          </div>
          <button
            onClick={clearFile}
            className="p-1 hover:bg-green-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-green-600" />
          </button>
        </div>
      ) : (
        <div
          {...getRootProps()}
          className={cn(
            'dropzone',
            isDragActive && 'dropzone-active',
            isDragAccept && 'dropzone-accept',
            isDragReject && 'dropzone-reject'
          )}
        >
          <input {...getInputProps()} accept={accept} />
          <Upload className="w-10 h-10 text-gray-400 mx-auto mb-3" />
          <p className="text-sm font-medium text-gray-700">
            {isDragActive ? 'Drop the file here' : 'Drag & drop or click to upload'}
          </p>
          <p className="text-xs text-gray-500 mt-1">{description}</p>
        </div>
      )}
    </div>
  );
}
