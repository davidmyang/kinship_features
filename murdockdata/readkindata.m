% codes in AT10.cod

file = textread('kinterm_adjusted.txt','%s','delimiter','\n','whitespace','');

is = 9:574; 
for iind = 1:length(is)
  i = is(iind);
  s = file{i};
  codes = {s(25:26), s(28:29), s(31:32), s(34:35), s(37:38), s(40:41), s(43:44), s(46:47), s(49:50), s(52:53), s(55:56), s(58:59), s(61:62), s(64:65)}; 
  for j = 1:14
    n = str2num(codes{j});
    if isempty(n) 
      n = 0;
    end
    allbutinlawcodes(iind,j) = n;
  end
end

save('kindata', 'allbutinlawcodes');

