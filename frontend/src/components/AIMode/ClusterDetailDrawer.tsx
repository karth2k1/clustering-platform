import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getClusterDetails, getNoisePoints } from '../../services/api';
import '../common/styles.css';

interface ClusterDetailDrawerProps {
  resultId: string;
  clusterId: number;
  clusterInfo: any;
  isOpen: boolean;
  onClose: () => void;
}

function ClusterDetailDrawer({ 
  resultId, 
  clusterId, 
  clusterInfo, 
  isOpen, 
  onClose 
}: ClusterDetailDrawerProps) {
  const [selectedAlarmIndex, setSelectedAlarmIndex] = useState<number | null>(null);

  const isNoisePoints = clusterId === -1;
  
  const { data: clusterDetails, isLoading } = useQuery({
    queryKey: isNoisePoints ? ['noise-points', resultId] : ['cluster-details', resultId, clusterId],
    queryFn: () => isNoisePoints ? getNoisePoints(resultId) : getClusterDetails(resultId, clusterId),
    enabled: isOpen,
  });

  if (!isOpen) return null;

  const selectedAlarm = selectedAlarmIndex !== null && clusterDetails?.alarms 
    ? clusterDetails.alarms[selectedAlarmIndex] 
    : null;

  return (
    <>
      {/* Backdrop */}
      <div className="drawer-backdrop" onClick={onClose} />
      
      {/* Drawer */}
      <div className="drawer-container">
        <div className="drawer-header">
          <div>
            <h2>{isNoisePoints ? 'Unique Cases (Noise Points)' : `Cluster ${clusterId} Details`}</h2>
            <p className="drawer-subtitle">{clusterInfo?.description}</p>
          </div>
          <button className="drawer-close" onClick={onClose}>×</button>
        </div>

        <div className="drawer-content">
          {isLoading ? (
            <div className="loading">Loading cluster details...</div>
          ) : clusterDetails?.error ? (
            <div className="error">{clusterDetails.error}</div>
          ) : clusterDetails ? (
            <>
              {/* Clustering Explanation (for regular clusters) */}
              {!isNoisePoints && clusterDetails.clustering_explanation && (
                <div className="clustering-explanation-section">
                  <h3>{clusterDetails.clustering_explanation.title}</h3>
                  <p>{clusterDetails.clustering_explanation.description}</p>
                  <ul className="feature-list">
                    {clusterDetails.clustering_explanation.features.map((feature: string, idx: number) => (
                      <li key={idx}>{feature}</li>
                    ))}
                  </ul>
                  <p className="explanation-note">{clusterDetails.clustering_explanation.note}</p>
                </div>
              )}

              {/* Explanation Section (for noise points) */}
              {isNoisePoints && clusterDetails.explanation && (
                <div className="importance-section priority-info">
                  <h3>{clusterDetails.explanation.title}</h3>
                  <p className="importance-summary">{clusterDetails.explanation.description}</p>
                  <ul className="importance-reasons-list">
                    {clusterDetails.explanation.reasons.map((reason: string, idx: number) => (
                      <li key={idx}>{reason}</li>
                    ))}
                  </ul>
                  <p className="explanation-note"><strong>Recommendation:</strong> {clusterDetails.explanation.recommendation}</p>
                  {clusterDetails.code_distribution && Object.keys(clusterDetails.code_distribution).length > 0 && (
                    <div className="code-distribution">
                      <strong>Alarm Code Distribution:</strong>
                      <div className="code-tags">
                        {Object.entries(clusterDetails.code_distribution).map(([code, count]: [string, any]) => (
                          <span key={code} className="code-tag">
                            {code}: {count}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Importance Section */}
              {clusterDetails.importance && !isNoisePoints && (
                <div className={`importance-section priority-${clusterDetails.importance.priority}`}>
                  <h3>Why This Cluster Matters</h3>
                  <p className="importance-summary">{clusterDetails.importance.summary}</p>
                  <div className="importance-reasons">
                    {clusterDetails.importance.reasons.map((reason: any, idx: number) => (
                      <div key={idx} className="importance-reason">
                        <span className="reason-icon">
                          {reason.type === 'severity' ? '⚠️' : 
                           reason.type === 'size' ? '📊' : 
                           reason.type === 'pattern' ? '🔍' : 'ℹ️'}
                        </span>
                        <div>
                          <strong>{reason.title}</strong>
                          <p>{reason.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Records List */}
              <div className="alarms-section">
                <h3>
                  {isNoisePoints 
                    ? `Unique ${clusterDetails.terminology?.plural || 'Records'} (${clusterDetails.alarm_count} total${clusterDetails.unique_alarm_codes ? `, ${clusterDetails.unique_alarm_codes} unique codes` : ''})`
                    : `${clusterDetails.terminology?.plural || 'Records'} in This Cluster (${clusterDetails.alarm_count})`
                  }
                </h3>
                <div className="alarms-list">
                  {clusterDetails.alarms.map((alarm: any, idx: number) => (
                    <div 
                      key={idx}
                      className={`alarm-item ${selectedAlarmIndex === idx ? 'selected' : ''}`}
                      onClick={() => setSelectedAlarmIndex(idx)}
                    >
                      <div className="alarm-item-header">
                        <span className={`severity-badge severity-${alarm.severity.toLowerCase()}`}>
                          {alarm.severity}
                        </span>
                        <span className="alarm-code">{alarm.code}</span>
                        <span className="alarm-name">{alarm.name}</span>
                      </div>
                      <div className="alarm-item-preview">
                        <span className="alarm-preview-text">{alarm.description}</span>
                        <span className="alarm-preview-object">{alarm.affected_mo_display_name}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Alarm Detail View */}
              {selectedAlarm && (
                <div className="alarm-detail-panel">
                  <div className="alarm-detail-header">
                    <h4>Alarm Details</h4>
                    <button 
                      className="close-detail-btn"
                      onClick={() => setSelectedAlarmIndex(null)}
                    >
                      ×
                    </button>
                  </div>
                  
                  <div className="alarm-detail-content">
                    {/* Alarm Information */}
                    <div className="detail-section">
                      <h5>Alarm Information</h5>
                      <div className="detail-grid">
                        <div className="detail-item">
                          <label>Code:</label>
                          <span>{selectedAlarm.code}</span>
                        </div>
                        <div className="detail-item">
                          <label>Name:</label>
                          <span>{selectedAlarm.name}</span>
                        </div>
                        <div className="detail-item">
                          <label>Severity:</label>
                          <span className={`severity-badge severity-${selectedAlarm.severity.toLowerCase()}`}>
                            {selectedAlarm.severity}
                          </span>
                        </div>
                        <div className="detail-item">
                          <label>Description:</label>
                          <span>{selectedAlarm.description}</span>
                        </div>
                        <div className="detail-item">
                          <label>Acknowledge Status:</label>
                          <span>{selectedAlarm.acknowledge}</span>
                        </div>
                        <div className="detail-item">
                          <label>Created:</label>
                          <span>{selectedAlarm.create_time}</span>
                        </div>
                        <div className="detail-item">
                          <label>Last Transition:</label>
                          <span>{selectedAlarm.last_transition_time}</span>
                        </div>
                      </div>
                    </div>

                    {/* Affected Object Information */}
                    <div className="detail-section">
                      <h5>Affected Object</h5>
                      <div className="detail-grid">
                        <div className="detail-item">
                          <label>Object Type:</label>
                          <span>{selectedAlarm.affected_mo_type}</span>
                        </div>
                        <div className="detail-item">
                          <label>Display Name:</label>
                          <span>{selectedAlarm.affected_mo_display_name}</span>
                        </div>
                        <div className="detail-item">
                          <label>Object ID:</label>
                          <span className="monospace">{selectedAlarm.affected_mo_id}</span>
                        </div>
                        {selectedAlarm.affected_mo_details && (
                          <>
                            <div className="detail-item">
                              <label>MOID:</label>
                              <span className="monospace">{selectedAlarm.affected_mo_details.moid}</span>
                            </div>
                            <div className="detail-item">
                              <label>Object Type (Detailed):</label>
                              <span>{selectedAlarm.affected_mo_details.object_type}</span>
                            </div>
                            {selectedAlarm.affected_mo_details.link && (
                              <div className="detail-item full-width">
                                <label>Link:</label>
                                <a 
                                  href={selectedAlarm.affected_mo_details.link} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="external-link"
                                >
                                  {selectedAlarm.affected_mo_details.link}
                                </a>
                              </div>
                            )}
                          </>
                        )}
                      </div>
                    </div>

                    {/* Additional Information */}
                    {selectedAlarm.additional_info && Object.keys(selectedAlarm.additional_info).length > 0 && (
                      <div className="detail-section">
                        <h5>Additional Information</h5>
                        <div className="detail-grid">
                          {Object.entries(selectedAlarm.additional_info).slice(0, 10).map(([key, value]) => (
                            <div key={key} className="detail-item">
                              <label>{key}:</label>
                              <span>{String(value)}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </>
          ) : null}
        </div>
      </div>
    </>
  );
}

export default ClusterDetailDrawer;

