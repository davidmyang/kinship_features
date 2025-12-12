function [partition, idmap] = murdockcode(sysind,code1, code2)

% PARTITION: partition corresponding to the two-part Murdock code (CODE1,
% CODE2). Includes NaN if the codes represent missing data, Inf if the
% partition is underspecified in some other way.

% IDMAP: each row (t, e) indicates that term t in the given partition must
% match a term for individual e which is external to the partition. e's
% label is an absolute reference based on the labeling of the master tree.

idmap = zeros(0,2);

switch sysind
  %------------------------------------------------------------
  case 1, % Grandparents: [9:12,65:68] in master tree
    switch code1
      case 0, % Missing
        partition = nan*ones(1,8);
      case 1, % Bisexual
        switch code2
	  case 1, % bisexual
	    partition = [1 2 1 2 1 2 1 2];
	  case 2, % bisexual variant with separate terms for GrFa(ms),
		  % GrFa(ws), GrMo
	    partition = [1 2 1 2 1 3 1 3];
	  otherwise
	    disp('unknown gp code2');
	end
      case 2, % Merging
	switch code2
	  case 3, % merging
	    partition = [1 1 1 1 1 1 1 1];
	  case 4, %  merging variant with separate term for MoMo only,
	    partition = [1 2 2 2 1 2 2 2];
	  case 5, %  merging variant with separate term for MoMo(ws) only,
	    partition = [1 2 2 2 2 2 2 2];
	  case 6, %  merging variant with separate terms for FaFa(ms) and
		  %  FaFa (ws) 
	    partition = [1 1 1 2 1 1 1 3];
	  otherwise
	    disp('unknown gp code2');
	end
      case 3, % Bifurcate Bisexual
        switch code2
	  case 7, % bifurcate bisexual
	    partition = [1 2 3 4 1 2 3 4];
	  case 8, %  bifurcate bisexual with single term for MoFa and FaMo
	    partition = [1 2 2 3 1 2 2 3];
	  case 9, %  bifurcate bisexual with separate terms for FaFa(ms)
		   %    and FaFa(ws)
	    partition = [1 2 3 4 1 2 3 5];
	  otherwise
	    disp('unknown gp code2');
	end
      case 4, % Matri-skewed
        switch code2
	  case 10, % matri-skewed
	    partition = [1 2 3 2 1 2 3 2];
	  otherwise
	    disp('unknown gp code2');
	end
      case 5, % Null
        switch code2
	  case 11, % null
	    partition = [1 2 1 2 1 2 1 2];
	    idmap = [idmap; 1, 15; 2, 20]; 
	  case 12, %  null with special term for GrFa, GrMo being 
		   %    called "mother" 
	    partition = [1 2 1 2 1 2 1 2];
	    idmap = [idmap; 1, 15]; 
	  case 13, %  null with special term for GrMo, GrFa being 
		   %    called "father" 
	    partition = [1 2 1 2 1 2 1 2];
	    idmap = [idmap; 2, 20]; 
	  otherwise
	    disp('unknown gp code2');
	end
      case 6, % Bifurcate
        switch code2
	  case 14, % bifurcate
	    partition = [1 1 2 2 1 1 2 2];
	  otherwise
	    disp('unknown gp code2');
	end
      case 7, % Patri-skewed
        switch code2
	  case 15, % patri-skewed
	    partition = [1 2 1 3 1 2 1 3];
	  otherwise
	    disp('unknown gp code2');
	end
      case 8,  % Rare
        switch code2
	  case 16, % distinguishing GrPa (ms) and GrPa (ws)
	    partition = [1 1 1 1 2 2 2 2];
	  otherwise
	    disp('unknown gp code2');
	end
      case 9,  % Rare
        switch code2
	  case 17, % distinguishing GrPa of ego's sex and GrPa of opposite sex
	    partition = [1 2 1 2 2 1 2 1];
	  otherwise
	    disp('unknown gp code2');
	end
      case 10, % Rare
        switch code2
	  case 18, %  distinguishing GrPa of Ego's sex, GrFa (ws), and GrMo (ms)
	    partition = [1 2 1 2 3 1 3 1];
	  otherwise
	    disp('unknown gp code2');
	end
      case 11, % Rare
        switch code2
	  case 19, % intermediate between bifurcate bisexual and bifurcate, 
		   % distinguishing FaPa, MoFa, and MoMo 
	    partition = [1 2 3 3 1 2 3 3];
	  otherwise
	    disp('unknown gp code2');
	end
      case 12, % Rare
        switch code2
	  case 20, % intermediate between bifurcate bisexual and bifurcate, 
		   % distinguishing FaFa, FaMo, and MoPa 
	    partition = [1 1 2 3 1 1 2 3];
	  otherwise
	    disp('unknown gp code2');
	end
      case 13, % Rare
        switch code2
	  case 21, % distinguishing GrFa (ms), GrFa (ws), GrMo (ms), GrMo(ws)
	    partition = [1 2 1 2 3 4 3 4];
	  otherwise
	    disp('unknown gp code2');
	end
      case 14, % Rare
        switch code2
	  case 22, % distinguishing FaFa (ms), FaFa (ws), MoFa, FaMo, MoMo (ms)
	  	   %	and MoMo (ws) 
	    partition = [1 2 3 4 5 2 3 6];
	  otherwise
	    disp('unknown gp code2');
	end
      otherwise
        disp('unknown gp code1');
    end  
  %------------------------------------------------------------
  case 2, % Grandchildren: [53:56,109:112] in master tree
    switch code1
      case 0, % Missing
        partition = nan*ones(1,8);
      case 1, % Merging
        switch code2
	  case 1, % merging
	    partition = [1 1 1 1 1 1 1 1 ];
	  case 2, % merging variant with separate terms for SoCh (ms) and
		  %   DaCh(ms) only
            % XXX: paper and kinterm.txt disagree
	    % partition = [1 1 2 2 2 2 3 3];
	    partition = [1 1 1 1 2 2 3 3];
	  otherwise
	    disp('unknown gc code2');
	end
      case 2, % Bisexual
        switch code2
	  case 3, % bisexual
	    partition = [1 2 1 2 1 2 1 2];
	  otherwise
	    disp('unknown gc code2');
	end
      case 3, % Self-reciprocal
	switch code2
	  case 4, % self-reciprocal
	    % XXX: will need to detect this later and use grandparent code
	    %	   to create partition
	    partition = [-1 -1 -1 -1 -1 -1 -1 -1];
	  case 5, % self-reciprocal pattern variant (underspecified)
	    partition = inf*ones(1,8);
	  otherwise
	    disp('unknown gc code2');
	end
      case 4, % Bifurcate bisexual
        switch code2
	  case 6, % bisexual
	    partition = [1 2 3 4 1 2 3 4];
	  otherwise
	    disp('unknown gc code2');
	end
      case 5, % Null
        switch code2
	  case 7, % null
	    partition = [1 2 1 2 1 2 1 2];
	    idmap = [idmap; 1, 47; 2, 48]; 
	  otherwise
	    disp('unknown gc code2');
	end
      case 6, % Speaker's sex
        switch code2
	  case 8, % speaker's sex
	    partition = [1 1 1 1 2 2 2 2];
	  otherwise
	    disp('unknown gc code2');
	end
      case 7, % Bifurcate
        switch code2
	  case 9, % bifurcate
	    partition = [1 1 2 2 1 1 2 2];
	  otherwise
	    disp('unknown gc code2');
	end
      case 8, % Bifurcate speaker's sex
	switch code2
	  case 10, % bifurcate speaker's sex
	    partition = [1,1,2,2,3,3,4,4];
	  case 11, % bifurcate speaker's sex variant: a man's SoCh
		   % further distinguished as SoSo (ms) and SoDa (ms)
	    partition = [1,1,2,2,3,3,4,5];
	  case 12, % Bifurcate speaker's sex pattern variant: SoCh (ws) 
		   % equated with DaCh (ms) 
	    partition = [1,1,2,2,2,2,3,3];
	  otherwise
	    disp('unknown gc code2');
	end
      case 9,  % Rare
        switch code2
	  case 13, % intermediate between bifurcate bisexual and
		   % bifurcate, distinguishing SoCh,  DaSon, and DaDa
	    partition = [1 2 3 3 1 2 3 3];
	  otherwise
	    disp('unknown gc code2');
	end
      case 10, % Rare
        switch code2
	  case 14, % intermediate between bifurcate and bifurcate speaker's sex,		   % distinguishing SoCh, DaCh (ms), and DaCh (ws)
	    partition = [1 1 2 2 3 3 2 2];
	  otherwise
	    disp('unknown gc code2');
	end
      case 11, % Rare
        switch code2
	  case 15, % distinguishing GrSo (ms), GrDa (ms), and GrCh (ws) 
	    partition = [1 1 1 1 2 3 2 3];
	  otherwise
	    disp('unknown gc code2');
	end
      case 12, % Rare
        switch code2
	  case 16, % distinguishing GrCh (ms), GrSo (ws), and GrDa (ws) 
	    partition = [1 2 1 2 3 3 3 3];
	  otherwise
	    disp('unknown gc code2');
	end
      case 13, % Rare
        switch code2
	  case 17, % distinguishing GrSo (ms), GrSo (ws), GrDa (ms), GrDa (ws) 
	    partition = [1 2 1 2 3 4 3 4];
	  otherwise
	    disp('unknown gc code2');
	end
      case 14, % Rare
        switch code2
	  case 18, % distinguishing SoCh, DaCh (ms), DaSo (ws), and DaDa (ws) 
	    partition = [1 2 3 3 4 4 3 3];
	  otherwise
	    disp('unknown gc code2');
	end
      case 15, % Rare
        switch code2
	  case 19, % distinguishing SoSo (ms), SoDa (ms), SoCh (ws) = DaCh (ms),		   % DaSo (ws), and DaDa (ws) 
	    partition = [1,2,3,3,4,4,5,6];
	  otherwise
	    disp('unknown gc code2');
	end
      case 16, % Rare
        switch code2
	  case 20, % maximal differentiation 
	    partition = [1,2,3,4,5,6,7,8];
	  otherwise
	    disp('unknown gc code2');
	end
      otherwise
        disp('unknown gc code1');
    end  
  %------------------------------------------------------------
  case 3, % Uncles: [16:17,21:22,72:73,77:78] in master tree
    switch code1
      case 0, % Missing
        partition = nan*ones(1,8);
      case 1, % Bifurcate merging
        switch code2
	  case 1, % bifurcate merging
	    partition = [1,1,2,2,1,1,2,2];
	    idmap = [idmap; 2, 20]; 
	  otherwise
	    disp('unknown un code2');
	end
      case 2, % Bifurcate collateral
	switch code2
	  case 2, % bifurcate collateral
	    partition = [1,1,2,2,1,1,2,2];
	  otherwise
	    disp('unknown un code2');
	end
      case 3, % Skewed bifurcate collateral
        switch code2
	  case 3, % skewed bifurcate collateral
	    partition = [1,1,2,3,1,1,2,3];
	  otherwise
	    disp('unknown un code2');
	end
      case 4, % Lineal
        switch code2
	  case 4, % lineal
	    partition = [1,1,1,1,1,1,1,1];
	  case 5, % lineal pattern variant: separate terms for male and female 
		  % speaker
	    partition = [1,1,1,1,2,2,2,2];
	  otherwise
	    disp('unknown un code2');
	end
      case 5, % Generation pattern
        switch code2
	  case 6, % generation pattern
	    partition = [1,1,1,1,1,1,1,1];
	    idmap = [idmap; 1, 20]; 
	  otherwise
	    disp('unknown un code2');
	end
      case 6, % Age-differentiated bifurcate collateral
        switch code2
	  case 7, % age differentiated bifurcate collateral
	    partition = [1,2,3,4,1,2,3,4];
	  case 8, % age differentiated bifurcate collateral variant
	    partition = [1,2,3,4,1,2,3,4];
	    idmap = [idmap; 3, 20]; 
	  otherwise
	    disp('unknown un code2');
	end
      case 7, % Relative age
        switch code2
	  case 9, % relative age
	    partition = [1,2,1,2,1,2,1,2];
	  otherwise
	    disp('unknown un code2');
	end
      case 8,  % Speaker-differentiated bifurcate merging
        switch code2
	  case 10, % speaker-differentiated bifurcate merging
	    partition = [1,1,2,2,3,3,2,2];
	    idmap = [idmap; 2, 20]; 
	  otherwise
	    disp('unknown un code2');
	end
      case 9,  % Speaker-differentiated bifurcate collateral 
        switch code2
	  case 11, % speaker-differentiated bifurcate collateral 
	    partition = [1,1,2,2,3,3,2,2];
	  case 12, % speaker-differentiated bifurcate collateral variant: 
		   % paternal uncles further distinguished as FaElBr and FaYoBr
	    partition = [1,1,2,3,4,4,2,3];
	  otherwise
	    disp('unknown un code2');
	end
      case 10, % Rare
        switch code2
	  case 13, % intermediate between age-differentiated bifurcate
		   % collateral and relative age, distinguishing PaElBr, 
		   % FaYoBr, and MoYoBr
	    partition = [1,2,3,2,1,2,3,2];
	  otherwise
	    disp('unknown un code2');
	end
      otherwise
        disp('unknown un code1');
    end  
  %------------------------------------------------------------
  case 4, % Aunt: [13:14,18:19,69:70,74:75] in master tree
    switch code1
      case 0, % Missing
        partition = nan*ones(1,8);
      case 1, % Bifurcate collateral
	switch code2
	  case 1, % bifurcate collateral
	    partition = [1,1,2,2,1,1,2,2];
	  otherwise
	    disp('unknown au code2');
	end
      case 2, % Bifurcate merging
        switch code2
	  case 2, % bifurcate merging
	    partition = [1,1,2,2,1,1,2,2];
	    idmap = [idmap; 1, 15]; 
	  case 3, % bifurcate merging
	    partition = [1,1,2,2,1,1,3,3];
	    idmap = [idmap; 1, 15]; 
	  otherwise
	    disp('unknown au code2');
	end
      case 3, % Lineal
        switch code2
	  case 4, % lineal
	    partition = [1,1,1,1,1,1,1,1];
	  otherwise
	    disp('unknown au code2');
	end
      case 4, % Generation pattern
        switch code2
	  case 5, % generation pattern
	    partition = [1,1,1,1,1,1,1,1];
	    idmap = [idmap; 1, 15]; 
	  otherwise
	    disp('unknown au code2');
	end
      case 5, % Skewed bifurcate collateral
        switch code2
	  case 6, % skewed bifurcate collateral
	    partition = [1,2,3,3,1,2,3,3];
	  case 7, % skewed bifurcate collateral variant: MoYoSi equated
		  % with mother
	    partition = [1,2,3,3,1,2,3,3];
	    idmap = [idmap; 1, 15]; 
	  otherwise
	    disp('unknown au code2');
	end
      case 6, % Relative age
        switch code2
	  case 8, % relative age
	    partition = [1,2,1,2,1,2,1,2];
	  otherwise
	    disp('unknown au code2');
	end
      case 7, % Age-differentiated bifurcate collateral
        switch code2
	  case 9, % age differentiated bifurcate collateral
	    partition = [1,2,3,4,1,2,3,4];
	  otherwise
	    disp('unknown au code2');
	end
      case 8,  % Speaker-differentiated bifurcate collateral 
        switch code2
	  case 10, % speaker-differentiated bifurcate collateral 
	    partition = [1,1,2,2,1,1,3,3];
	  otherwise
	    disp('unknown au code2');
	end
      case 9, % Rare
        switch code2
	  case 11, % distinguishing PaSi (ms) and PaSi (ws) 
	    partition = [1,1,1,1,2,2,2,2];
	  otherwise
	    disp('unknown au code2');
	end
      case 10, % Rare
        switch code2
	  case 12, % intermediate between A and L, distinguishing FaElSi, 
		   %  FaYoSi, and MoSi 
            % wrong initially:
	    %partition = [1,1,1,1,2,2,3,3];
	    partition = [1,1,2,3,1,1,2,3];
	  otherwise
	    disp('unknown au code2');
	end
      case 11, % Rare
        switch code2
	  case 13, % intermediate between K and R, distinguishing PaElSi,
		   % FaYoSi, and MoYoSi 
	    partition = [1,2,3,2,1,2,3,2];
	  otherwise
	    disp('unknown au code2');
	end
      case 12, % Rare
        switch code2
	  case 14, % intermediate between L and R, distinguishing FaElSi,
	           %  MoElSi, and PaYoSi
	    partition = [1,2,1,3,1,2,1,3];
	  otherwise
	    disp('unknown au code2');
	end
      otherwise
        disp('unknown au code1');
    end  
  %------------------------------------------------------------
  case 5, % nephewsnieces: [99:102,105:108] in master tree
    switch code1
      case 0, % Missing
        partition = nan*ones(1,8);
      case 1, % Bifurcate merging
	switch code2
	  case 1, % bifurcate merging
	    partition = [1,1,1,1,2,3,2,3];
	    idmap = [idmap; 2, 103; 3,104]; 
	  case 2, % bifurcate merging variant: SiSo alone distinguished
		  % terminologically from own child
	    partition = [1,2,1,2,1,3,1,3];
	    idmap = [idmap; 1, 103; 3,104]; 
	  case 3, % bifurcate merging variant: SiDa alone distinguished
		  % terminologically from own child
	    partition = [1,2,1,2,3,2,3,2];
	    idmap = [idmap; 2, 104; 3,103]; 
	  case 4, % bifurcate merging variant: ElSiCh alone distinguished
		  % terminologically from own child
	    partition = [1,2,3,3,1,2,1,2];
	    idmap = [idmap; 1, 103; 2,104]; 
	  otherwise
	    disp('unknown nn code2');
	end
      case 2, % Sex-differentiated bifurcate merging
        switch code2
	  case 5, % sex-differentiated bifurcate merging
	    partition = [1,2,1,2,3,4,3,4];
	    idmap = [idmap; 3, 103; 4,104]; 
	  otherwise
	    disp('unknown nn code2');
	end
      case 3, % Simple bifurcate collateral
        switch code2
	  case 6, % bifurcate collateral
	    partition = [1,1,1,1,2,2,2,2];
	  otherwise
	    disp('unknown nn code2');
	end
      case 4, % Lineal
        switch code2
	  case 7, % lineal
	    partition = [1,1,1,1,1,1,1,1];
	  case 8, % lineal variant: nieces only distinguished from own child, 
	          % nephews equated with sons 
	    partition = [1,2,1,2,1,2,1,2];
	    idmap = [idmap; 2, 104]; 
	  otherwise
	    disp('unknown nn code2');
	end
      case 5, % Generation
        switch code2
	  case 9, % generation
	    partition = [1,2,1,2,1,2,1,2];
	    idmap = [idmap; 1, 103; 2, 104]; 
	  otherwise
	    disp('unknown nn code2');
	end
      case 6, % Sex-differentiated lineal
        switch code2
	  case 10, % sex-differentiated lineal
	    partition = [1,2,1,2,1,2,1,2];
	  otherwise
	    disp('unknown nn code2');
	end
      case 7, % Sex-differentiated bifurcate collateral
        switch code2
	  case 11, % sex-differentiated bifurcate collateral
	    partition = [1,2,1,2,3,4,3,4];
	  otherwise
	    disp('unknown nn code2');
	end
      case 8,  % Age-skewed bifurcate collateral 
        switch code2
	  case 12, % age-skewed bifurcate collateral 
	    partition = [1,1,1,1,2,2,3,3];
	  case 13, % age-skewed bifurcate collateral variant 
	    partition = [1,2,1,2,3,3,4,4];
	  otherwise
	    disp('unknown nn code2');
	end
      case 9, % Age-differentiated bifurcate collateral
        switch code2
	  case 14, % age-differentiated bifurcate collateral
	    partition = [1,1,2,2,3,3,4,4];
	  case 15, % age-differentiated bifurcate collateral variant: ElBrCh 
		   % further distinguished as ElBrSo and ElBrDa 
	    partition = [1,1,2,2,3,3,4,5];
	  case 16, % age-differentiated bifurcate collateral variant: ElBrCh 
		   % equated with the speaker's own child
	    partition = [1,1,2,2,3,3,4,5];
	    idmap = [idmap; 4, 103; 5, 104]; 
	  otherwise
	    disp('unknown nn code2');
	end
      case 10, % Sister-skewed bifurcate collateral
        switch code2
	  case 17, % sister-skewed bifurcate collateral
	    partition = [1,2,1,2,3,3,3,3];
	  otherwise
	    disp('unknown nn code2');
	end
      case 11, % Brother-skewed bifurcate collateral
        switch code2
	  case 18, % brother-skewed bifurcate collateral
	    partition = [1,1,1,1,2,3,2,3];
	  otherwise
	    disp('unknown nn code2');
	end
      case 12, % Rare
        switch code2
	  case 19, % distinguishing ElSbCh and YoSiCh by relative age only
	    partition = [1,1,2,2,1,1,2,2];
	  otherwise
	    disp('unknown nn code2');
	end
      case 13, % Rare
        switch code2
	  case 20, % distinguishing BrSo, SiSo, and SbDa 
	    partition = [1,2,1,2,1,3,1,3];
	  otherwise
	    disp('unknown nn code2');
	end
      case 14, % Rare
        switch code2
	  case 21, %distinguishing ElBrSo=SiSo, YoSbSo, and SbDa 
	    partition = [1,2,1,2,1,3,1,2];
	  otherwise
	    disp('unknown nn code2');
	end
      case 15, % Rare
        switch code2
	  case 22, % distinguishing ElSbSo, ElSbDa, YoSbSo, and YoSbDa
	    partition = [1,2,3,4,1,2,3,4];
	  otherwise
	    disp('unknown nn code2');
	end
      case 16, % Rare
        switch code2
	  case 23, %  distinguishing ElSbSo, YoBrSo, ElBrDa, and YoBrDa, SiCh 
	    partition = [1,1,1,1,2,3,4,5];
	  otherwise
	    disp('unknown nn code2');
	end
      case 17, % Rare
        switch code2
	  case 24, % distinguishing ElBrCh, YoBrCh, YoBrDa, ElSiSo=SiDa, YoSiDa
	           % can't code
	    partition = inf*ones(1,8);
	  otherwise
	    disp('unknown nn code2');
	end
      case 18, % Rare
        switch code2
	  case 25, % distinguishing ElBrSo, YoBrSo, ElBrDa, YoBrDa, SiSo,SiDa 
	    partition = [1,2,1,2,3,4,5,6];
	  otherwise
	    disp('unknown nn code2');
	end
      case 19, % Rare
        switch code2
	  case 26, % maximally differentiated
	    partition = [1,2,3,4,5,6,7,8];
	  otherwise
	    disp('unknown nn code2');
	end
      otherwise
        disp('unknown nn code1');
    end  
  %------------------------------------------------------------
  case 6, % siblings: [31:34,87:90] in master tree
    switch code1
      case 0, % Missing
        partition = nan*ones(1,8);
      case 1, % Dravidian
	switch code2
	  case 1, % dravidian
	    partition = [1,2,3,4,1,2,3,4];
	  case 2, % dravidian variant: ElBr further distinguished as ElBr (ms) 
		  % and ElBr (ws)
	    partition = [1,2,3,4,1,2,3,5];
	  case 3, % dravidian variant: YoBr further distinguished as YoBr (ms) 
		  % and YoBr (ws) 
	    partition = [1,2,3,4,1,2,5,4];
	  case 4, % dravidian variant: YoSi further distinguished as YoSi (ms) 
		  % and YoSi (ws) 
	    partition = [1,2,3,4,5,2,3,4];
	  case 5, % dravidian variant: Si(ms) further distinguished from YoSi, 
		  % ElSi 
	    partition = [1,2,3,4,5,5,3,4];
	  case 6, % dravidian variant: YoSi(ws) equated with YoBr rather than 
		  % with YoSi (ms) 
	    partition = [1,2,1,3,4,2,1,3];
	  case 7, % dravidian variant: YoBr(ms) equated with YoSi rather than 
		  % with YoBr (ws) 
	    partition = [1,2,3,4,1,2,1,4];
	  case 8, % dravidian variant: YoBr(ws) equated with YoSi rather than 
		  % with YoBr (ms) 
	    partition = [1,2,1,3,1,2,4,3];
	  otherwise
	    disp('unknown sib code2');
	end
      case 2, % European
        switch code2
	  case 9, % european
	    partition = [1,1,2,2,1,1,2,2];
	  case 10, % european variant: separate terms for Br (ms) and Br (ws)
	    partition = [1,1,2,2,1,1,3,3];
	  otherwise
	    disp('unknown sib code2');
	end
      case 3, % Yoruban
        switch code2
	  case 11, % yoruban 
	    partition = [1,2,1,2,1,2,1,2];
	  case 12, % yoruban variant: separate term for Si (ms) 
	    partition = [1,2,1,2,3,3,1,2];
	  case 13, % yoruban variant: YoSb distinguished as YoBr(ms), YoSi(ms) 
		   % and YoSb(ws) 
	    partition = [1,2,1,2,3,2,4,2];
	  otherwise
	    disp('unknown sib code2');
	end
      case 4, % Algonkian
        switch code2
	  case 14, % algonkian
	    partition = [1,2,1,3,1,2,1,3];
	  case 15, % algonkian variant: ElBr distinguished as ElBr(ms) and 
		   % ElBr(ws)
	    partition = [1,2,1,3,1,2,1,4];
	  otherwise
	    disp('unknown sib code2');
	end
      case 5, % Kordofanian
        switch code2
	  case 16, % kordofanian
	    partition = [1,1,1,1,1,1,1,1];
	  otherwise
	    disp('unknown sib code2');
	end
      case 6, % Southern Bantu
        switch code2
	  case 17, % southern bantu
	    partition = [1,2,3,3,3,3,1,2];
	  case 18, % southern bantu variant: YoSb of speaker's sex further 
		   % distinguished as YoBr (ms) and YoSi (ws)
	    partition = [1,2,3,3,3,3,4,2];
	  case 19, % southern bantu variant: ElSb of speaker's sex further 
		   % distinguished as ElBr (ms) and ElSi (ws)
	    partition = [1,2,3,3,3,3,1,4];
	  otherwise
	    disp('unknown sib code2');
	end
      case 7, % East Polynesian
        switch code2
	  case 20, % east polynesian
	    partition = [1,2,3,3,4,4,1,2];
	  otherwise
	    disp('unknown sib code2');
	end
      case 8, % Quechuan
        switch code2
	  case 21, % quechuan
	    partition = [1,1,2,2,3,3,4,4];
	  case 22, % quechuan variant: Br (ms) further distinguished as 
		   % ElBr (ms) and YoBr (ms)
	    partition = [1,1,2,2,3,3,4,5];
	  otherwise
	    disp('unknown sib code2');
	end
      case 9, % Carolinian
        switch code2
	  case 23, % carolinian
	    partition = [1,1,2,2,2,2,1,1];
	  otherwise
	    disp('unknown sib code2');
	end
      case 10, % Siouan
        switch code2
	  case 24, % siouan
	    partition = [1,2,3,4,5,6,7,8];
	  case 25, % siouan variant: underspecified
	    partition = inf*ones(1,8);
	  otherwise
	    disp('unknown sib code2');
	end
      case 11, % Caddoan
        switch code2
	  case 26, % caddoan
	    partition = [1,2,3,3,4,4,5,6];
	  case 27, % caddoan variant:YoBr (ms) equated with YoSi (ws)
	    partition = [1,2,3,3,4,4,1,5];
	  case 28, % caddoan variant:YoBr (ms) equated with Br (ws)
	    partition = [1,2,3,3,4,4,3,6];
	  otherwise
	    disp('unknown sib code2');
	end
      case 12, % Malagasy
        switch code2
	  case 29, % malagasy
	    partition = [1,1,2,2,3,3,1,1];
	  case 30, % malagasy variant: Br (ws) further distinguished as
	           %  ElBr (ws) and YoBr (ws)
	    partition = [1,1,2,3,4,4,1,1];
	  otherwise
	    disp('unknown sib code2');
	end
      case 13, % Jivaran
        switch code2
	  case 31, % jivaran
	    partition = [1,1,2,2,2,2,3,3];
	  case 32, % jivaran variant: Br (ms) further distinguished as
	           % ElBr (ms) and YoBr (ms)
	    partition = [1,1,2,2,2,2,3,4];
	  otherwise
	    disp('unknown sib code2');
	end
      case 14, % Voltaic
        switch code2
	  case 33, % voltaic
	    partition = [1,1,2,3,1,1,2,3];
	  case 34, % voltaic variant: Si distinguished as Si (ms) Si (ws)
	    partition = [1,1,2,3,4,4,2,3];
	  case 35, % voltaic variant:  ElBr distinguished as ElBr (ms) ElBr (ws)
	    partition = [1,1,2,3,1,1,2,4];
	  otherwise
	    disp('unknown sib code2');
	end
      case 15, % Yukian
        switch code2
	  case 36, % yukian
	    partition = [1,2,3,2,1,2,3,2];
	  otherwise
	    disp('unknown sib code2');
	end
      case 16, % Rare
        switch code2
	  case 37, % rare: distinguishing Br (ms), Br (ws), ElSi, and YoSi 
	    partition = [1,2,3,3,1,2,4,4];
	  otherwise
	    disp('unknown sib code2');
	end
      case 17, % Rare
        switch code2
	  case 38, % rare: distinguishing ElBr=YoBr (ws), ElSi (ws), Si (ms),
	           % and YoSb of the speaker's sex
	    partition = [1,2,3,3,4,4,1,3];
	  otherwise
	    disp('unknown sib code2');
	end
      case 18, % Rare
        switch code2
	  case 39, % rare: distinguishing ElBr (ms), YoBr (ms), ElSi (ws),
	           %       YoSi (ws), and sibling of the opposite sex
	    partition = [1,2,3,3,3,3,4,5];
	  otherwise
	    disp('unknown sib code2');
	end
      case 19, % Rare
        switch code2
	  case 40, % rare: distinguishing ElBr (ms), ElBr (ws), YoBr, Si (ms),
	           %       and Si (ws)

	    partition = [1,1,2,3,4,4,2,5];
	  otherwise
	    disp('unknown sib code2');
	end
      case 20, % rare
        switch code2
	  case 41, % rare: distinguishing ElBr (ms), ElBr (ws), YoBr, ElSi,
	           %       and YoSi=YoBr (ws) 
	    partition = [1,2,1,3,1,2,4,5];
	  otherwise
	    disp('unknown sib code2');
	end
      case 21, % rare
        switch code2
	  case 42, % rare:  distinguishing ElBr (ms), ElBr (ws), YoBr=YoSi (ws),
		   %        ElSi (ws), and Si (ms) 
	    partition = [1,2,1,3,4,4,1,5];
	  otherwise
	    disp('unknown sib code2');
	end
      case 22, % rare
        switch code2
	  case 43, % rare:  distinguishing ElSb of the speaker's sex, YoSb of
	           %     the speaker's sex, ElBr (ws), YoBr (ws), ElSi (ms), 
		   %	 and YoSi (ms)
	    partition = [1,2,3,4,5,6,1,2];
	  otherwise
	    disp('unknown sib code2');
	end
      otherwise
        disp('unknown sib code1');
  end
  %------------------------------------------------------------
  case 7, % cross cousins: [23:30,35:42,79:86,91:98] in master tree
	  % always choose an older sibling for idmap
    switch code1
      case 0, % Missing
        partition = nan*ones(1,32);
      case 1, % Hawaiian
	switch code2
	  case 1, % hawaiian
	    partition = [repmat([1,3,2,4,1,3,2,4], 1,2),...
			 repmat([5,7,6,8,5,7,6,8], 1,2)];
	    idmap = [idmap; 1, 31; 2, 32; 3, 33; 4, 34;...
			    5, 87; 6, 88; 7, 89; 8, 90]; 
	  otherwise
	    disp('unknown cc code2');
	end
      case 2, % Iroquois
        switch code2
	  case 2, % iroquois
	    partition = [1,3,2,4,9,9,9,9,9,9,9,9,1,3,2,4,...
			 5,7,6,8,9,9,9,9,9,9,9,9,5,7,6,8];
	    idmap = [idmap; 1, 31; 2, 32; 3, 33; 4, 34;...
			    5, 87; 6, 88; 7, 89; 8, 90]; 
	  case 3, % combination of iroquois and Hawaiian features
	    partition = inf*ones(1,32); % underspecified
	  otherwise
	    disp('unknown cc code2');
	end
      case 3, % Eskimo
        switch code2
	  case 4, % eskimo
	    partition = 9*ones(1,32);
	  case 5, % combination of eskimo and Hawaiian features
	    partition = inf*ones(1,32); % underspecified
	  case 6, % combination of eskimo and iroquois features
	    partition = inf*ones(1,32); % underspecified
	  otherwise
	    disp('unknown cc code2');
	end
      case 4, % Omaha
        switch code2
%http://www.umanitoba.ca/faculties/arts/anthropology/tutor/kinterms/dani.html 
	  case 7, % omaha
	    partition = [1,3,2,4, 9,10, 9,10,11,12,11,12,1,3,2,4,...
			 5,7,6,8,15,16,15,16,13,14,13,14,5,7,6,8];
	    idmap = [idmap; 1, 31; 2, 32; 3, 33; 4, 34;...
			    5, 87; 6, 88; 7, 89; 8, 90;...
			    9, 15; 10,17; 11,47; 12,48; 13, 101; 14, 102;...
			    15,71; 16,73]; 

	  case 8, % omaha variant
	    partition = inf*ones(1,32); % underspecified
	  case 9, % omaha variant
	    partition = inf*ones(1,32); % underspecified
	  case 10, % omaha variant
	    partition = inf*ones(1,32); % underspecified
	  otherwise
	    disp('unknown cc code2');
	end

      case 5 % Crow
        switch code2
	  case 11, % crow
	    partition = [1,3,2,4, 9,10, 9,10,11,12,11,12,1,3,2,4,...
			 5,7,6,8,13,14,13,14,15,16,15,16,5,7,6,8];
	    idmap = [idmap; 1, 31; 2, 32; 3, 33; 4, 34;...
			    5, 87; 6, 88; 7, 89; 8, 90;...
			    9,51; 10,52; 11,19; 12,20; 13, 103; 14, 104;...
			    15,75; 16,76]; 

	  case 12, % crow variant
	    partition = inf*ones(1,32); % underspecified
	  case 13, % crow variant
	    partition = inf*ones(1,32); % underspecified
	  case 14, % crow variant
	    partition = inf*ones(1,32); % underspecified
	  otherwise
	    disp('unknown cc code2');
	end

      case 6 % Descriptive
        switch code2
	  case 15, % descriptive
	    partition = [1,2,1,2,3,4,3,4,5,6,5,6,7,8,7,8,...
			 1,2,1,2,3,4,3,4,5,6,5,6,7,8,7,8];
	  otherwise
	    disp('unknown cc code2');
	end

      case 7 % Sudanese
        switch code2
	  case 16, % sudanese
	    partition = [1,2,1,2,3,4,3,4,5,6,5,6,7,8,7,8,...
			 1,2,1,2,3,4,3,4,5,6,5,6,7,8,7,8];
	  case 17, % sudanese variant
	    partition = inf*ones(1,32); % underspecified
	  case 18, % sudanese variant
	    partition = inf*ones(1,32); % underspecified
	  otherwise
	    disp('unknown cc code2');
	end
      otherwise
        disp('unknown cc code1');
    end  
  %------------------------------------------------------------
  case 8, % F, M, S, D  [15,20,71,76,47,48,103,104] in master tree
    partition = [1,2,1,2,3,4,3,4];
  otherwise
        disp('unknown pt code1');
  end
end



