import { useMutation, useQuery } from '@tanstack/react-query';
import { createNotebook, getNotebookSession } from '../../services/api';
import '../common/styles.css';

interface NotebookLauncherProps {
  fileId: string;
}

function NotebookLauncher({ fileId }: NotebookLauncherProps) {
  const createMutation = useMutation({
    mutationFn: createNotebook,
  });

  const handleCreateNotebook = () => {
    createMutation.mutate(fileId);
  };

  const { data: session } = useQuery({
    queryKey: ['notebook-session', createMutation.data?.session_id],
    queryFn: () => getNotebookSession(createMutation.data?.session_id || ''),
    enabled: !!createMutation.data?.session_id,
  });

  return (
    <div className="card">
      <h2>Jupyter Notebook Playground</h2>
      <p className="section-description">
        Create a Jupyter notebook with pre-populated analysis code for the selected data file.
      </p>

      {!createMutation.data ? (
        <div>
          <button
            className="button"
            onClick={handleCreateNotebook}
            disabled={createMutation.isPending}
          >
            {createMutation.isPending ? 'Creating Notebook...' : 'Create Notebook'}
          </button>

          {createMutation.isError && (
            <div className="error">
              Failed to create notebook: {createMutation.error instanceof Error ? createMutation.error.message : 'Unknown error'}
            </div>
          )}
        </div>
      ) : (
        <div className="notebook-ready">
          <div className="success">
            Notebook created successfully!
          </div>
          <div className="notebook-info">
            <p><strong>Session ID:</strong> {createMutation.data.session_id}</p>
            <p><strong>Notebook URL:</strong></p>
            <a
              href={createMutation.data.notebook_url}
              target="_blank"
              rel="noopener noreferrer"
              className="button"
              style={{ display: 'inline-block', marginTop: '0.5rem' }}
            >
              Open in JupyterLab →
            </a>
          </div>
          {session && (
            <div className="session-info">
              <p><strong>Status:</strong> {session.status}</p>
              {session.kernel_id && (
                <p><strong>Kernel ID:</strong> {session.kernel_id}</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default NotebookLauncher;

