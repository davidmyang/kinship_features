% Make the master file of realworld partitions

load('kindata');

[uu,ii,jj] = unique(allbutinlawcodes, 'rows');
freqs = transpose(hist(jj, 1:max(jj)));
[s,sind] = sort(freqs, 'descend');

% matrix with encountered patterns and their frequencies (column 1)
a = [freqs(sind), uu(sind,:)];

% Create a cell array to store original row indices for each unique pattern
original_rows = cell(length(uu), 1);
for i = 1:length(uu)
    original_rows{i} = find(jj == i);
end
% Sort the original_rows according to frequency ranking
sorted_original_rows = original_rows(sind);


% all indices here refer to the 114 individuals in the master tree
ept = zeros(1,114);  % empty partition
gpind =    [9:12,65:68];
gcind =    [53:56,109:112];
uncleind = [16:17,21:22,72:73,77:78];
auntind  = [13:14,18:19,69:70,74:75];
nepind = [99:102,105:108];
sibind=  [31:34,87:90];
couind = [23:30,35:42,79:86,91:98];
ptind =  [15,20,71,76,47,48,103,104];

% needed to decode some grandparent codes
reciprocal = ept;
reciprocal(gpind) = [53,109,55,111,54,110,56,112];
reciprocal(gcind) = [9,65,11,67,10,66,12,68];

thisorder= 1:112;

rws = zeros(size(a,1), length(thisorder));

for i = 1:size(a,1)
  [gp, gpid] = murdockcode(1, a(i,2), a(i,3)); 
  [gc, gcid] = murdockcode(2, a(i,4), a(i,5)); 
  [unc, uncid] = murdockcode(3, a(i,6), a(i,7)); 
  [ant, antid] = murdockcode(4, a(i,8), a(i,9)); 
  [nep, nepid] = murdockcode(5, a(i,10), a(i,11)); 
  [sib, sibid] = murdockcode(6, a(i,12), a(i,13)); 
  [cou, couid] = murdockcode(7, a(i,14), a(i,15)); 
  pt = murdockcode(8, 0, 0);

  p = nan*ones(size(ept));

  p(ptind) = pt;

  p(gpind) = gp+10;
  gpid(:,1) = gpid(:,1)+10;

  p(gcind) = gc + 20;
  gcid(:,1) = gcid(:,1)+20;

  p(uncleind) = unc+30;
  uncid(:,1) = uncid(:,1)+30;

  p(auntind) = ant+40;
  antid(:,1) = antid(:,1)+40;

  p(nepind) = nep+50;
  nepid(:,1) = nepid(:,1)+50;

  p(sibind) = sib+60;
  sibid(:,1) = sibid(:,1)+60;

  p(couind) = cou+70;
  couid(:,1) = couid(:,1)+70;

  if sum(gc < 0) % specification using reciprocal
    p(gcind) = p(reciprocal(gcind));
  end

  for k = 1:size(gpid,1)
    code = gpid(k,1);
    p(p==code)=p(gpid(k,2));
  end

  for k = 1:size(gcid,1)
    code = gcid(k,1);
    p(p==code)=p(gcid(k,2));
  end

  for k = 1:size(uncid,1)
    code = uncid(k,1);
    p(p==code)=p(uncid(k,2));
  end
  for k = 1:size(antid,1)
    code = antid(k,1);
    p(p==code)=p(antid(k,2));
  end
  for k = 1:size(nepid,1)
    code = nepid(k,1);
    p(p==code)=p(nepid(k,2));
  end
  for k = 1:size(sibid,1)
    code = sibid(k,1);
    p(p==code)=p(sibid(k,2));
  end
  for k = 1:size(couid,1)
    if ~isinf(p(couid(k,2))) && ~isnan(p(couid(k,2))) 
			     % because some cousin codes set identity wrt
			     % niblings, for which data are incomplete
      code = couid(k,1);
      p(p==code)=p(couid(k,2));
    end
  end

  thisp = p(thisorder);
  thisp(thisp==inf) = nan;
  rws(i,:) = canonicallabel(thisp);
  freqs(i) = a(i,1);
end

rws(isnan(rws)) = -1;

[uu,ii,jj] = unique(rws, 'rows');

final_original_rows = cell(length(uu), 1);

for i = 1:length(ii)
  repeatind = find(jj==i);
  newfreqs(i) = sum(freqs(repeatind));

  % Combine original row indices for patterns that got merged
  combined_rows = [];
  for j = 1:length(repeatind)
    combined_rows = [combined_rows; sorted_original_rows{repeatind(j)}];
  end
  final_original_rows{i} = combined_rows;
end

[s,sind] = sort(newfreqs, 'descend');
% first column will now store frequencies
finalpartitions = [transpose(s), uu(sind,:)];

final_sorted_original_rows = final_original_rows(sind);

% write frequencies and partitions to file
fid = fopen('rwpartitions.txt', 'w');

for i = 1:size(finalpartitions,1)
  fprintf(fid, '%4d', finalpartitions(i,:));
  fprintf(fid, '\n');
end
fclose(fid);

% Create mapping matrix: [original_row_index, final_system_index]
mapping = [];
for k = 1:length(final_sorted_original_rows)
    original_indices = final_sorted_original_rows{k};  % Extract vector from cell k
    final_pattern_indices = repmat(k, length(original_indices), 1);  % Create matching pattern indices
    mapping = [mapping; original_indices, final_pattern_indices];  % Concatenate to mapping matrix
end

% Sort by original row index for easier reading
mapping = sortrows(mapping, 1);

% Write to file
writematrix(mapping, 'system_mapping.txt', 'Delimiter', '\t');

