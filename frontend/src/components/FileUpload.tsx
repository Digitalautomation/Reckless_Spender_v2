import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

function FileUpload() {
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [message, setMessage] = useState<string>('');
    const [error, setError] = useState<string>('');

    const onDrop = useCallback((acceptedFiles: File[]) => {
        // Only take the first file if multiple are dropped
        if (acceptedFiles.length > 0) {
            const file = acceptedFiles[0];
            // Basic validation for OFX extension
            if (file.name.toLowerCase().endsWith('.ofx')) {
                setUploadedFile(file);
                setMessage(`Selected file: ${file.name}`);
                setError(''); // Clear previous errors
            } else {
                setUploadedFile(null);
                setError('Invalid file type. Please upload an .ofx file.');
                setMessage('');
            }
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
             'application/ofx': ['.ofx'], // Standard OFX MIME type
             'application/x-ofx': ['.ofx'] // Common alternative
        },
        multiple: false, // Allow only single file upload
    });

    const handleUpload = async () => {
        if (!uploadedFile) {
            setError('Please select a file first.');
            return;
        }

        setIsLoading(true);
        setMessage('Uploading...');
        setError('');

        const formData = new FormData();
        formData.append('file', uploadedFile); // 'file' must match the name expected by FastAPI

        try {
            // TODO: Replace with environment variable for API URL
            const response = await fetch('http://localhost:8000/upload/ofx', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                // Throw an error with the detail message from the API if possible
                throw new Error(result.detail || `HTTP error! status: ${response.status}`);
            }

            setMessage(`Upload successful: ${result.message || 'File processed.'} (${result.accounts_processed} accounts, ${result.transactions_collected} transactions)`);
            setUploadedFile(null); // Clear selection after successful upload
        } catch (err: any) {
            console.error("Upload error:", err);
            setError(`Upload failed: ${err.message || 'Unknown error'}`);
            setMessage('');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container mx-auto p-4 max-w-md">
            <h2 className="text-2xl font-semibold mb-4 text-center text-gray-800 dark:text-gray-200">Upload OFX File</h2>
            <div 
                {...getRootProps()} 
                className={`p-8 border-2 border-dashed rounded-lg cursor-pointer text-center transition-colors duration-200 ease-in-out 
                           ${isDragActive 
                             ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30' 
                             : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}
                           ${error ? 'border-red-500' : ''}
                          `}
            >
                <input {...getInputProps()} />
                {
                    isDragActive ?
                        <p className="text-blue-600 dark:text-blue-400">Drop the file here ...</p> :
                        <p className="text-gray-500 dark:text-gray-400">Drag 'n' drop an OFX file here, or click to select</p>
                }
                
            </div>
            {uploadedFile && (
                <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">
                    Selected: {uploadedFile.name}
                </div>
            )}
            {error && (
                <div className="mt-4 text-sm text-red-600 dark:text-red-400">
                    Error: {error}
                </div>
            )}
            {message && !error && (
                <div className="mt-4 text-sm text-green-600 dark:text-green-400">
                    {message}
                </div>
            )}
            <button 
                onClick={handleUpload}
                disabled={!uploadedFile || isLoading}
                className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 ease-in-out"
            >
                {isLoading ? 'Uploading...' : 'Upload File'}
            </button>
        </div>
    );
}

export default FileUpload; 