def checkBipDist(reader,pairs,thresh=20):
    from cmlreaders import CMLReader
    from scipy.spatial import distance
    
    # Function to check the distance between the individual elecs in bipolar pairs
    # Returns boolean array of True or False
    if isinstance(pairs,pd.DataFrame):
        results = np.ones(len(pairs),dtype='bool')
    elif isinstance(pairs,pd.Series):
        results = True
    
    # Try to load monopolar contacts
    try:
        monos = reader.load("contacts")
    except:
        print('cannot load contacts for subject',reader.subject)
        return results
    
    if 'avg.corrected.x' in pairs:
        xcoord, ycoord, zcoord = 'avg.corrected.x','avg.corrected.y','avg.corrected.z'
    elif 'avg.dural.x' in pairs:
        xcoord, ycoord, zcoord = 'avg.dural.x','avg.dural.y','avg.dural.z'
    else:
        xcoord, ycoord, zcoord = 'avg.x','avg.y','avg.z'
            
    # Calculate the distance between each bipolar pair contact
    if isinstance(pairs,pd.DataFrame):
        bip_dists = []
        for p, pair in pairs.iterrows():
            coord_a = monos[monos.contact==pair['contact_1']][[xcoord, ycoord, zcoord]]
            coord_b = monos[monos.contact==pair['contact_2']][[xcoord, ycoord, zcoord]]
            try:
                bip_dist = distance.euclidean(coord_a,coord_b)
            except:
                bip_dist = np.nan

            bip_dists.append(bip_dist)
            results[p] = bip_dist < thresh
    elif isinstance(pairs,pd.Series):
        coord_a = monos[monos.contact==pairs['contact_1']][[xcoord, ycoord, zcoord]]
        coord_b = monos[monos.contact==pairs['contact_2']][[xcoord, ycoord, zcoord]]
        try:
            bip_dists = distance.euclidean(coord_a,coord_b)
        except:
            bip_dists = np.nan

        results = bip_dist < thresh
        
    return results, bip_dists