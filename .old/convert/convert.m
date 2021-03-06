addpath(genpath('~/csi/project/src/convert/functions'))

csi_trace = read_bf_file(argv(){1});
% eliminate empty cell
xx = find(cellfun('isempty', csi_trace));
csi_trace(xx) = [];

% Extract CSI information for each packet
fprintf('Have CSI for %d packets\n', length(csi_trace))

% Scaled into linear
csi = zeros(length(csi_trace),1,30);
timestamp = zeros(1,length(csi_trace));
temp = [];

for packet_index = 1:length(csi_trace)
    scaled_csi = get_scaled_csi(csi_trace{packet_index})
    if size(scaled_csi)(1,2) == 1
        last_successful = scaled_csi
    else
        scaled_csi = last_successful
    end
    csi(packet_index,:,:) = scaled_csi
    timestamp(packet_index) = csi_trace{packet_index}.timestamp_low * 1.0e-6;
end
timestamp = timestamp';

% File export
csi_amp_matrix = permute(db(abs(squeeze(csi))), [2 3 1]);
csi_phase_matrix = permute(angle(squeeze(csi)), [2 3 1]);

for k=1:size(csi_phase_matrix,2)
    for j=1:size(csi_phase_matrix,3)
        csi_phase_matrix2(:,k,j) = phase_calibration(csi_phase_matrix(:,k,j))';
    end
end

for packet_index = 1:length(csi_trace)
    temp = [temp;horzcat(reshape(csi_amp_matrix(:,:,packet_index)',[1,30]),...
                            reshape(csi_phase_matrix2(:,:,packet_index)',[1,30]))];
end
csvwrite(argv(){2},horzcat(timestamp,temp));