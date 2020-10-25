%DB Convert from decibels.
%
% (c) 2008-2011 Daniel Halperin <dhalperi@cs.washington.edu>
%
function ret = db(x)
    ret = 10*log(x/1);
end
